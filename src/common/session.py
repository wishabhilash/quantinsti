import redis

class Session(object):
    def __init__(self, account_id):
        self._r = redis.Redis()
        self.hset_name = self.get_hset_name(account_id)
        self._r.expire(self.hset_name, 34*60*60)            

    def exists(self):
        return self._r.exists(self.hset_name)
        
    def set(self, key, value):
        '''
        Set data to session.
        '''
        try:
            self._r.hset(self.hset_name, key, value)
        except Exception as e:
            return False
        return True
        
    def get(self, key):
        '''
        Get data from session.
        '''
        try:
            data = self._r.hget(self.hset_name, key)
        except Exception as e:
            return None
        return data
    
    def get_hset_name(self, account_id):
        '''
        Creates the hset name to be used.
        '''
        return "%s:%s" % ("session", account_id)

    def clear(self):
        '''
        Clear the session.
        '''
        self._r.delete(self.hset_name)