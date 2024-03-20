"""
  更新存储桶中的对象
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


# 替换存储桶中的对象
bucket_name = 'my-new-bucket'
object_key = '《深空彼岸》.txt'
new_file_path = "E:\\下载\\《深空彼岸》.txt"
s3_client.upload_file(new_file_path, bucket_name, object_key)
print(f'Object {object_key} in {bucket_name} updated.')