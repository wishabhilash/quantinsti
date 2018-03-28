from src.celery_app import celery_app as app
from random import random
import uuid
from src.broker import Broker
from src.datamanager import DataManager

broker = Broker()


@app.task
def get_quotes(instrument, timestamp, lookback):
    dm = DataManager(instrument)
    data = dm.query(timestamp, lookback)
    return [item['close'] for item in data]

@app.task
def execute_order(account_id, instrument, quantity, price, signal, order_id=None):
    ##### TODO ####
    # Create or update order for user account_id

    if signal == 'buy':
        broker.buy(account_id, instrument, quantity, price, signal, order_id)
    else:
        broker.sell(account_id, instrument, quantity, price, signal, order_id)

