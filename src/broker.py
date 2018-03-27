from random import random

class Broker(object):
    def buy(self):
        return self._get_order_status()

    def sell(self):
        return self._get_order_status()

    def _get_order_status(self):
        result = int(random() * 10) % 2
        return 'pass' if not result else 'fail'
