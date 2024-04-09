import boto3
from botocore.client import Config

# 创建一个连接
s3 = boto3.resource(
    's3',
    endpoint_url='http://localhost:9000',  # 你的MinIO服务器地址
    aws_access_key_id='youraccesskey',  # 你的访问键
    aws_secret_access_key='yoursecretkey',  # 你的密钥
    config=Config(signature_version='s3v4'),
)

# 创建一个新的存储桶（如果它不存在的话）
bucket_name = 'mybucket'
if not s3.Bucket(bucket_name) in s3.buckets.all():
    s3.create_bucket(Bucket=bucket_name)

# 上传一个文件
file_name = '1.txt'  # 你要上传的文件名
s3.Bucket(bucket_name).upload_file(file_name, 'myfile_in_s3.txt')

# 下载刚才上传的文件
s3.Bucket(bucket_name).download_file('myfile_in_s3.txt', 'myfile_downloaded.txt')
