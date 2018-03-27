from src.celery_app import celery_app as app
from random import random
import uuid
from src.broker import Broker

broker = Broker()

@app.task
def get_quotes(instrument, timestamp, lookback):
    return "quote"

@app.task
def execute_order(account_id, instrument, quantity, signal):
    ##### TODO ####
    # Create or update order for user account_id

    return broker.buy() if signal == 'BUY' else broker.sell()



@app.task
def get_user(userid, initial_capital):
    #### TODO ####
    # Get or create user
    pass