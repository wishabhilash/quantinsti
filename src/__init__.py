import os
import sys

# Load project into system path
# so that all the modules can be called
# from the root of the project.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.settings import Config

config = Config()
    
def start_celery():
    from src.celery_app import celery_app
    celery_app.start(argv=['celery', 'worker', '-l', 'info', '--concurrency=1'])

def start_ticker(args):
    from src.ticker import Ticker
    ticker = Ticker(args['interval'])
    ticker.run()

def start_strategy(args):
    import importlib
    try:
        _strategy = importlib.import_module("src.strategy.%s" % args['name'])
    except ImportError as e:
        raise ImportError('Strategy with the name "%s" doesn\'t exist.' % args['name'])

    strategy = _strategy.Algorithm(args)
    strategy.run()

def sync_models(args):
    from src.models import mysql_db as db
    from src.models import User, Order
    db.create_tables([User, Order])



def execute(args):
    if args['command'] == "celery":
        start_celery()
    elif args['command'] == "ticker":
        start_ticker(args)
    elif args['command'] == "strategy":
        start_strategy(args)
    elif args['command'] == "sync":
        sync_models(args)
    