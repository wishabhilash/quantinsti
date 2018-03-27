import redis

class Service(object):
    
    def __init__(self, *args):
        self.channels = list(args)
        self._r = redis.Redis()
        self.pubsub = self._r.pubsub()    

    def subscribe(self):
        '''
        Subscribe to a list of channels.
        '''
        if not isinstance(self.channels, list):
            raise TypeError('Subscription channels must be in a <list>.')
        self.pubsub.subscribe(channels)
        print('Consumer started')
        self._on_data()

    def publish(self, data):
        '''
        Publish data to the first channel provided during instanciation of this object.
        '''
        if not isinstance(self.channels, list):
            raise TypeError('Publication channel must be a <str>.')

        if not self.channels:
            raise IndexError("No channels provided to publish into.")

        self._r.publish(self.channels[0], data)

    def _on_data(self):
        for item in self.pubsub.listen():
            self.on_data(item['data'])

    def on_data(self, data):
        '''
        Override this method to work with the 
        fetched data from the subscribed channels.
        '''
        pass

