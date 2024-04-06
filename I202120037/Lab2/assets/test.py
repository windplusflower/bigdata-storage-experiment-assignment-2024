import boto3

# 修改为您的Access Key和Secret Key
access_key = '8XUw990Grl7L6JcBeG7l'
secret_key = '5rhdPHmVKwOXi0AVCGrJ0t6GUpLlP00KRqrHGYX1'

# 修改为Minio Server正在运行的网址
endpoint_url = 'http://127.0.0.1:9000'

# 创建Boto3客户端
s3 = boto3.client('s3', endpoint_url=endpoint_url, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# 获取所有存储桶
response = s3.list_buckets()

# 打印所有存储桶
print("Existing buckets:")
for bucket in response['Buckets']:
    print(f"  {bucket['Name']}")