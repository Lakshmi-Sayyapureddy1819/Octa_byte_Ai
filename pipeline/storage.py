import json
import os
import gzip
from datetime import datetime
from utils.helpers import get_logger
import boto3

class LocalStorage:
    """Saves data to the local filesystem."""
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

class S3Storage:
    """Saves data to AWS S3."""
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')
        self.logger = get_logger(self.__class__.__name__)

    def save(self, data, source, data_type='raw'):
        date_str = datetime.now().strftime('%Y-%m-%d')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        s3_key = f"{data_type}/{source}/{date_str}/{timestamp}.json.gz"

        try:
            json_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
            compressed_data = gzip.compress(json_bytes)
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=compressed_data,
                ContentEncoding='gzip',
                ContentType='application/json'
            )
            self.logger.info(f"Successfully saved data to s3://{self.bucket_name}/{s3_key}")
        except Exception as e:
            self.logger.error(f"Error saving data to S3: {e}")

def get_storage_clients(config):
    """Initializes all active storage clients based on the config."""
    clients = []
    active_providers = config.get("active", [])
    
    if "local" in active_providers:
        clients.append(LocalStorage(config["providers"]["local"]["base_path"]))
    
    if "aws" in active_providers:
        clients.append(S3Storage(config["providers"]["aws"]["bucket_name"]))
        
    return clients