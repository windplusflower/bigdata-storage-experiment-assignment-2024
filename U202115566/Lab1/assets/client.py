import boto3

# 创建 S3 客户端
s3 = boto3.client(
    's3',
    endpoint_url='http://127.0.0.1:8080'
)

# 创建存储桶
bucket_name = 'test'

s3.create_bucket(Bucket=bucket_name)

print("Bucket created successfully.")

# 列出所有存储桶
response = s3.list_buckets()

print("List of Buckets:")
for bucket in response['Buckets']:
    print(bucket['Name'])

