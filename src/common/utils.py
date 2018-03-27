import json

class StaticQueue(object):
    storage = []
    queue_size = None

    def __init__(self, queue_size=5):
        self.queue_size = queue_size

    def push(self, item):
        self.storage.append(item)
        if len(self.storage) > self.queue_size:
            self.storage.pop(0)

    def get_list(self):
        return self.storage

    def __len__(self):
        return len(self.storage)

    def __repr__(self):
        return json.dumps(self.storage)

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError("Key must be an int")
        try:
            return self.storage[key]
        except IndexError as e:
            raise e
