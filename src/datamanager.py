from src.settings import Config
import os
from src.common.utils import Singleton, str_if_bytes
from src.common.utils import StaticQueue
import redis
import json


config = Config()

class DataManager(object, metaclass=Singleton):
    def __init__(self, instrument):
        self.filepath = os.path.join(config.datafile_path, "%s.csv" % instrument)
        self._r = redis.Redis()
        self.instrument = instrument

    def query(self, date, lookback):
        # Check if data available in cache
        data = self._get_data_from_cache(date, lookback)
        if data is not None:
            return data
        return self._get_data_from_file(date, lookback)

    def _get_data_from_file(self, date, lookback):
        if not isinstance(lookback, int):
            raise TypeError("Lookback must be an <int>.")
        
        if lookback < 1:
            raise Exception('Lookback must be greater than 0.')

        queue = StaticQueue(lookback)

        with open(self.filepath) as f:
            for line in f:
                line = line.strip(" ").strip('\n')
                try:
                    line.index('null')
                    continue
                except ValueError as e:
                    queue.push(line)
                    if line.startswith(date):
                        break
        
        # Save retreived data to cache
        self._save_data_to_cache(queue.items(), date, lookback)

        # Return in json format
        return [self._convert_to_json(item) for item in queue.items()]
    

    def _get_data_from_cache(self, date, lookback):
        '''
        Cache for datamanager for optimised lookup.
        '''
        key = self._create_cache_key(date, lookback)
        try:
            data = self._r.get(key)
        except Exception as e:
            return None
        
        if data is None:
            return None

        json_data = json.loads(str_if_bytes(data)) if data is not None else None
        return [self._convert_to_json(item) for item in json_data]

    def _save_data_to_cache(self, data, date, lookback):
        '''
        Cache for datamanager for optimised lookup.
        '''
        key = self._create_cache_key(date, lookback)
        try:
            self._r.set(key, json.dumps(data))
        except Exception as e:
            return False
        return True

    def _create_cache_key(self, date, lookback):
        return "dm:%s:%s:%s:" % (self.instrument, date, lookback)

    def _convert_to_json(self, row):
        split_row = row.split(',')
        return {
            'timestamp': split_row[0],
            'open': float(split_row[1]),
            'high': float(split_row[2]),
            'low': float(split_row[3]),
            'close': float(split_row[4]),
            'adjusted_close': float(split_row[5]),
            'volume': int(split_row[6])
        }