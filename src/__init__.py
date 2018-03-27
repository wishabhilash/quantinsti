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
        _strategy = importlib.import_module("src.strategy.%s" % args['strategy_name'])
    except ImportError as e:
        raise e



def execute(args):
    if args['command'] == "celery":
        start_celery()
    elif args['command'] == "ticker":
        start_ticker(args)
    