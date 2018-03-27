from src.common.pubsub import Service
import time

class Ticker(Service):

    def __init__(self, interval, channels=*args):
        super().__init__(channels)
        self.interval = interval

    def run(self):
        while True:
            time.sleep(5000)
