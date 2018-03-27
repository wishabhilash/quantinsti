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

    # Strategy
    strategy_parser = subparsers.add_parser('strategy')
    strategy_parser.add_argument(
        'name',
        help="Name of the strategy.",
        type=str
    )

    strategy_parser.add_argument(
        'userid',
        help="Users ID (a new user is created if user doesn't exist).",
        type=str
    )

    strategy_parser.add_argument(
        '-c',
        '--capital',
        help="Initial capital for a new user.",
        default=100000,
        type=int
    )

    strategy_parser.add_argument(
        '-s',
        '--start_date',
        help="Start date for strategy; format yyyy-mm-dd.",
        default=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    )

    strategy_parser.add_argument(
        '-e',
        '--end_date',
        help="End date for strategy; format yyyy-mm-dd.",
        default=datetime.now().strftime('%Y-%m-%d')
    )

    strategy_parser.add_argument(
        '-sp',
        '--sma_period',
        help="Period for SMA.",
        default=5
    )

    strategy_parser.add_argument(
        '-lp',
        '--lma_period',
        help="Period for SMA.",
        default=20
    )

    args = vars(parser.parse_args())
    print(args)
    import src
    src.execute(args)
