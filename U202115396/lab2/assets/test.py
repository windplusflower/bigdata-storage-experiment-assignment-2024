import boto3

# 替换为您的 Minio 访问密钥 ID 和秘密访问密钥
access_key = 'your-access-key'
secret_key = 'your-secret-key'

# 指定 Minio Server 的端点 URL
endpoint_url = 'your-minio-server.com'

# 创建一个 Boto3 S3 客户端实例
s3_client = boto3.client(
    's3',
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)

# 现在您可以使用 s3_client 来执行对 Minio 的操作
# 列出所有的存储桶
buckets = s3_client.list_buckets()

for bucket in buckets['Buckets']:
    print(bucket['Name'])