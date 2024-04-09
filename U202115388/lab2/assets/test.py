import boto3
from botocore.client import Config

# 指定Swift的S3兼容服务端点
endpoint_url = 'http://localhost:12345'

# 配置访问密钥和秘密密钥
access_key = 'test:tester'
secret_key = 'testing'

# 创建一个S3客户端实例
s3_client = boto3.client(
    's3',
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    config=Config(signature_version='s3v4'),  # 确保使用正确的签名版本
    region_name='us-east-1'  # 指定区域
)

# 执行操作（例如列出桶）
response = s3_client.list_buckets()
print(response['Buckets'])
print(f'Listed {len(response["Buckets"])} buckets.')
if len(response['Buckets']) == 0:
    print('No buckets found.')
else:
    print('Buckets:')
    for bucket in response['Buckets']:
        # 打印桶的名称以及对象
        print(f'Name: {bucket["Name"]}')
        response = s3_client.list_objects_v2(Bucket=bucket['Name'])
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f'Object: {obj["Key"]}')
        else:
            print('    No objects found.')
