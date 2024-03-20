"""
创建一个新的存储桶
"""

import boto3
# 指定 Minio Server 的access_key和secret_key
access_key = 'zrEx1EHiSHgMpvauncEf'
secret_key = 'uju0b7EZXgAlTVIG9Hgw6a0i0MqR8DUlWeAkp1yI'
# 初始化客户端
s3_client = boto3.client(
    's3',
    endpoint_url='http://127.0.0.1:9000',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

# 创建一个新的存储桶
bucket_name = 'my-new-bucket'
s3_client.create_bucket(Bucket=bucket_name)
print(f'Bucket {bucket_name} created.')