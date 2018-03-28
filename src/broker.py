from random import random
from src.models import User, Order
from src.models import mysql_db as db

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
                order = self._create_new_buy_order(account_id, instrument, quantity, price, trade_type)
            else:
                order = self._close_sell_orders(order_id, price)
            return {
                'order_id': str(order._id),
                'status': status
            }
        else:
            return {
                'order_id': None,
                'status': status
            }
    
    def _create_new_buy_order(self, account_id, instrument, quantity, price, trade_type):
        print("Creating new buy order")
        user = User.get(name=account_id)
        order = Order(
            user = user,
            instrument = instrument,
            quantity = quantity,
            trade_type = trade_type,
            buy_price = price,
            status = 'open'
        )

        user.fund = user.fund - quantity * price

        with db.atomic() as transaction:
            try:
                order.save()
                user.save()
                print("Passed buy")
            except Exception as identifier:
                transaction.rollback()
                print("Failed buy")
        return order

    def _close_sell_orders(self, order_id, price):
        print("Closing sell orders")
        order = Order.get(_id=order_id)
        order.sell_price = price
        order.status='close'
        user = order.user
        user.fund = order.sell_price * order.quantity

        with db.atomic() as transaction:
            try:
                order.save()
                user.save()
            except Exception as e:
                transaction.rollback()
        return order


    def sell(self, account_id, instrument, quantity, price, trade_type, order_id=None):
        '''
        If order_id is None a new order is created else
        sell_price and status of existing order is updated.
        '''
        status = self._get_order_status()
        if status == 'pass':
            order = None
            if order_id is None:
                order = self._create_new_sell_order(account_id, instrument, quantity, price, trade_type)
            else:
                order = self._close_buy_orders(order_id, price)
            return {
                'order_id': str(order._id),
                'status': status
            }
        else:
            return {
                'order_id': None,
                'status': status
            }

    def _create_new_sell_order(self, account_id, instrument, quantity, price, trade_type):
        print("Creating new sell orders")
        user = User.get(name=account_id)
        order = Order(
            user = user,
            instrument = instrument,
            quantity = quantity,
            trade_type = trade_type,
            sell_price = price,
            status = 'open'
        )

        user.fund = user.fund - quantity * price

        with db.atomic() as transaction:
            try:
                order.save()
                user.save()
            except Exception as identifier:
                transaction.rollback()
        return order

    def _close_buy_orders(self, order_id, price):
        print("Closing buy orders")
        order = Order.get(_id=order_id)
        order.buy_price = price
        order.status='close'
        user = order.user
        user.fund = order.buy_price * order.quantity

        with db.atomic() as transaction:
            try:
                order.save()
                user.save()
            except Exception as e:
                transaction.rollback()
        return order


    def _get_order_status(self):
        result = int(random() * 10) % 2
        return 'pass' if not result else 'fail'
