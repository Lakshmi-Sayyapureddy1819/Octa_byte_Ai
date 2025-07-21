import json
import os
from datetime import datetime
from utils.helpers import get_logger

class LocalStorage:
    def __init__(self, base_path):
        self.base_path = base_path
        self.logger = get_logger(self.__class__.__name__)
        os.makedirs(os.path.join(self.base_path, 'raw'), exist_ok=True)
        os.makedirs(os.path.join(self.base_path, 'processed'), exist_ok=True)

    def save(self, data, source, data_type='raw'):
        date_str = datetime.now().strftime('%Y-%m-%d')
        dir_path = os.path.join(self.base_path, data_type, source, date_str)
        os.makedirs(dir_path, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        file_path = os.path.join(dir_path, f"{timestamp}.json")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            self.logger.info(f"Successfully saved data to {file_path}")
        except IOError as e:
            self.logger.error(f"Error saving data to {file_path}: {e}")

def get_storage_client(config):
    if config['provider'] == 'local':
        return LocalStorage(config['local']['base_path'])
    # Add 'aws' provider logic here if you switch to S3
    # elif config['provider'] == 'aws':
    #     return S3Storage(...)
    else:
        raise ValueError("Unsupported storage provider")