from src.settings import Config
import os
from src.common.utils import Singleton
from src.common.utils import StaticQueue


config = Config()

class DataManager(object, metaclass=Singleton):
    def __init__(self, instrument):
        self.filepath = os.path.join(config.datafile_path, "%s.csv" % instrument)

    def query(self, date, lookback):
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
                queue.push(line)
                if line.startswith(date):
                    break
        
        # Save retreived data to cache
        self._save_data_to_cache(queue.items(), date, lookback)

        # Return in json format
        return [self._convert_to_json(item) for item in queue.items()]
    

    def _get_data_from_cache(self, date, lookback):
        return None

    def _save_data_to_cache(self, data, date, lookback):
        pass

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