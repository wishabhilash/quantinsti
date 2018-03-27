from random import random
from src.models import User, Order

class Broker(object):
    def buy(self, account_id, instrument, quantity, price, trade_type, order_id=None):
        '''
        If order_id is None a new order is created else
        buy_price and status of existing order is updated.
        '''
        
        status = self._get_order_status()
        if status == 'pass':
            order = None
            if order_id is None:
                user = User.get(name=account_id)
                order = Order(
                    user = user,
                    instrument = instrument,
                    quantity = quantity,
                    signal = 'sell',
                    trade_type = trade_type,
                    sell_price = price,
                    status = 'open'
                )
            else:
                order = order.get(_id=order_id)
                order.buy_price = price
                order.status='close'
            
            try:
                order.save()
            except Exception as e:
                raise e
            return {
                'order_id': str(order._id),
                'status': status
            }
        else:
            return {
                'order_id': None,
                'status': status
            }

    def sell(self, account_id, instrument, quantity, price, trade_type, order_id=None):
        '''
        If order_id is None a new order is created else
        sell_price and status of existing order is updated.
        '''
        status = self._get_order_status()
        if status == 'pass':
            order = None
            if order_id is None:
                user = User.get(name=account_id)
                order = Order(
                    user = user,
                    instrument = instrument,
                    quantity = quantity,
                    signal = 'sell',
                    trade_type = trade_type,
                    sell_price = price,
                    status = 'open'
                )
            else:
                order = order.get(_id=order_id)
                order.sell_price = price
                order.status='close'
            
            try:
                order.save()
            except Exception as e:
                raise e
            return {
                'order_id': str(order._id),
                'status': status
            }
        else:
            return {
                'order_id': None,
                'status': status
            }


    def _get_order_status(self):
        result = int(random() * 10) % 2
        return 'pass' if not result else 'fail'
