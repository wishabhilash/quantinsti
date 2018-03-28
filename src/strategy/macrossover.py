from src.common.pubsub import Service
from src.tasks import get_quotes, execute_order
from src.settings import Config
from datetime import datetime, timedelta
from src.models import User
from src.common import Session


class Algorithm(Service):
    current_date = None
    date_format = "%Y-%m-%d"

    def __init__(self, args):
        self.config = Config()
        
        super().__init__(self.config.ticker_channel)
        self.args = args
        self.start_date = self._sanitize_datetime(self.args['start_date'])
        self.end_date = self._sanitize_datetime(self.args['end_date'])
        self.user = self._get_user(args['userid'], args['capital'])

        # Create the user session
        self.session = Session(self.user.name)

        # If new session is created then update the fund
        if not self.session.exists():
            self.session.set('fund', self.user.fund)
    
    def _sanitize_datetime(self, timestamp):
        a = datetime.strptime(timestamp, self.date_format)
        return a.strftime(self.date_format)

    def _increment_date(self, date):
        _d = datetime.strptime(date, self.date_format)
        new_date = _d + timedelta(days=1)
        return new_date.strftime(self.date_format)

    def on_data(self, data):
        '''
        This is where tick data is received
        and further processing is done.
        '''
        if self.current_date is None:
            self.current_date = self.start_date
        else:
            self.current_date = self._increment_date(self.current_date)

        # Get close data results from DataManager
        result = get_quotes.delay(
            self.args['instrument'], 
            self.current_date, 
            self.args['lma_period']
        ).get()
        
        # Calculate sma and lma
        sma = self.ma(result, self.args['sma_period'])
        lma = self.ma(result, self.args['lma_period'])

        print(self.current_date, sma, lma, 'buy' if sma > lma else 'sell')
        result = self._place_order(sma, lma, result[-1])
        
        if self.current_date == self.args['end_date']:
            self.output_result()
            self.session.clear()
            exit()

    def _sell_or_close_order(self, sma, lma, price, quantity):
        results = []
        # Check if any open long orders exist
        orders = self.user.orders.filter(trade_type='long', status='open')
        if len(orders):
            for order in orders:
                result = execute_order.delay(
                    self.user.name, 
                    self.args['instrument'],
                    quantity,
                    price,
                    'buy',
                    order._id
                ).get()
                results.append(result)
        else:
            if not quantity:
                return False

            # Place order
            result = execute_order.delay(
                self.user.name, 
                self.args['instrument'],
                quantity,
                price,
                'sell'
            ).get()
            results.append(result)
        
        return results

    def _buy_or_close_order(self, sma, lma, price, quantity):
        results = []
        # Check if any open long orders exist
        orders = self.user.orders.filter(trade_type='short', status='open')
        if len(orders):
            for order in orders:
                result = execute_order.delay(
                    self.user.name, 
                    self.args['instrument'],
                    quantity,
                    price,
                    'sell',
                    order._id
                ).get()
                results.append(result)
        else:
            if not quantity:
                return None

            # Place order
            result = execute_order.delay(
                self.user.name, 
                self.args['instrument'],
                quantity,
                price,
                'buy'
            ).get()
            results.append(result)

        return results


    def _place_order(self, sma, lma, price):
        # If sma < lma then sell
        quantity = self.calculate_quantity_to_be_bought(price)
        
        if sma < lma:
            # Check if any open long orders exist
            self._sell_or_close_order(sma, lma, price, quantity)
            
        # If sma > lma then buy
        elif sma > lma:
            self._buy_or_close_order(sma, lma, price, quantity)
            
        
    def _get_user(self, account_id, initial_capital):
        '''
        Returns user if exists else creates new and returns user.
        '''
        try:
            user = User.get(name=account_id)
            return user
        except Exception as e:
            user = User(name=account_id, fund=initial_capital)
            user.save()
            return user

    def ma(self, data, period):
        '''
        Computes and returns the requisted moving average.
        '''
        sum = 0
        for i in data[-period:]:
            sum += i
        return sum/period

    def calculate_quantity_to_be_bought(self, price):
        return int(self.user.fund/price)

    def output_result(self):
        pass