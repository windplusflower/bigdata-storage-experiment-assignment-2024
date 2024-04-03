import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import logging

#logging.basicConfig(level=logging.DEBUG)

s3 = boto3.client('s3',
    aws_access_key_id='swift123:swift123',
    aws_secret_access_key='swift_key',
    config=Config(signature_version='s3v4'),
    endpoint_url='http://127.0.0.1:12345',
    use_ssl=False
)

try:
    response = s3.list_buckets()
    print(response)
except ClientError as e: 
    print(e.response)