import json

class StaticQueue(object):
    storage = []
    queue_size = None

    def __init__(self, queue_size=5):
        self.queue_size = queue_size

    def push(self, item):
        '''
        Pushes the new item to the right
        while popping the item on the left.
        '''
        self.storage.append(item)
        if len(self.storage) > self.queue_size:
            self.storage.pop(0)

    def bulk_push(self, *args):
        for item in args:
            self.push(item)

    def items(self):
        return self.storage

    def __len__(self):
        return len(self.storage)

    def __repr__(self):
        return json.dumps(self.storage)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.storage[key]
        elif isinstance(key, slice):
            return self.storage[key.start:key.stop:key.step]
        else:
            raise TypeError("Key must be of the type <int> or <slice>.")
        

class Singleton(type):
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instance

