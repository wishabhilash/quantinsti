from src.common.pubsub import Service
import time
from src.settings import Config

class Ticker(Service):
    publish_channel = ""

    def __init__(self, interval=5):
        self.config = Config()
        
        super().__init__(self.config.ticker_channel)
        self.interval = interval
        

    def run(self):
        '''
        Run the service with a delay of provided interval.
        '''
        print("Ticker started...")
        while True:
            self.publish("tick")
            print("tick")
            time.sleep(self.interval)

