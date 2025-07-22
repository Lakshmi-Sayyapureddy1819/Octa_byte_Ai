import unittest
import boto3
from moto import mock_aws
from pipeline.storage import S3Storage

@mock_aws
class TestS3Storage(unittest.TestCase):
    def test_save_to_s3(self):
        # Set up mock S3 environment
        s3 = boto3.client("s3", region_name="us-east-1")
        bucket_name = "test-bucket"
        s3.create_bucket(Bucket=bucket_name)

        # Test the save functionality
        storage = S3Storage(bucket_name)
        test_data = {"key": "value"}
        storage.save(test_data, "test_source", "raw")

        # Verify the object was created in the mock S3
        response = s3.list_objects_v2(Bucket=bucket_name)
        self.assertEqual(len(response['Contents']), 1)
        self.assertTrue(response['Contents'][0]['Key'].startswith("raw/test_source/"))