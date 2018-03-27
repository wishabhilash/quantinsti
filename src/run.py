import os
import sys
import argparse
from datetime import datetime, timedelta

# Load project into system path
# so that all the modules can be called
# from the root of the project.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # Celery
    celery_parser = subparsers.add_parser('celery')

    # Ticker
    ticker_parser = subparsers.add_parser('ticker')
    ticker_parser.add_argument(
        '-l',
        '--interval',
        type=int,
        default=5
    )

    

    args = vars(parser.parse_args())
    print(args)
    import src
    src.execute(args)
