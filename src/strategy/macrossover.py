from src.common.pubsub import Service
from src.tasks import get_quotes
from src.settings import Config
from datetime import datetime, timedelta


class Algorithm(Service):
    current_date = None
    date_format = "%Y-%m-%d"

    def __init__(self, args):
        self.config = Config()
        super().__init__(self.config.ticker_channel)
        self.args = args
        self.start_date = datetime.strptime(self.args['start_date'], self.date_format)
        self.end_date = datetime.strptime(self.args['end_date'], self.date_format)
        

    def on_data(self, data):

        if self.current_date is None:
            self.current_date = self.start_date
        else:
            self.current_date += timedelta(days=1)

        # Get close data results from DataManager
        result = get_quotes.delay(121, self.current_date, self.args['lma_period'])
        print(result.get())

        if self.current_date.strftime(self.date_format) == self.args['end_date']:
            exit()

        # while True:
        #     get_quotes.delay(
        #         121,
        #         ts,
        #         self.args['lma_period']
        #     )