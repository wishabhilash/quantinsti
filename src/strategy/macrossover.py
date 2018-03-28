from src.common.pubsub import Service
from src.tasks import get_quotes, execute_order
from src.settings import Config
from datetime import datetime, timedelta
from src.models import User


class Algorithm(Service):
    current_date = None
    date_format = "%Y-%m-%d"

    def __init__(self, args):
        self.config = Config()
        super().__init__(self.config.ticker_channel)
        self.args = args
        self.start_date = datetime.strptime(self.args['start_date'], self.date_format)
        self.end_date = datetime.strptime(self.args['end_date'], self.date_format)
        self.user = self._get_user(args['name'], args['initial_capital'])
        

    def on_data(self, data):
        if self.current_date is None:
            self.current_date = self.start_date
        else:
            self.current_date += timedelta(days=1)

        # Get close data results from DataManager
        result = get_quotes.delay(
            self.args['instrument'], 
            self.current_date, 
            self.args['lma_period']
        ).get()
        
        # Calculate sma and lma
        sma = self.ma(result, self.args['sma_period'])
        lma = self.ma(result, self.args['lma_period'])

        self._place_order(sma, lma, result[-1])
        
        if self.current_date.strftime(self.date_format) == self.args['end_date']:
            self.output_result()
            exit()

    def _place_order(self, sma, lma, price):
        # If sma < lma then sell
        if sma < lma:
            execute_order.delay(
                self.user.name, 
                self.args['instrument'],
                self.calculate_quantity_to_be_bought(price),
                'sell'
            )

        # If sma > lma then buy
        elif sma > lma:
            execute_order.delay(
                self.user.name, 
                self.args['instrument'],
                self.calculate_quantity_to_be_bought(price),
                'buy'
            )

        
    def _get_user(self, account_id, initial_capital):
        '''
        Returns user if exists else creates new and returns user.
        '''
        user = User.get(name=account_id)
        if user:
            return user
        else:    
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