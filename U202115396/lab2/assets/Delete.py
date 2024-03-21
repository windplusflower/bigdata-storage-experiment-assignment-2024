"""
删除对象和存储桶
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

# # 先更新一个新的对象
bucket_name = 'my-new-bucket'
# object_key = '《十日终焉》.txt'
# new_file_path = "E:\下载\《十日终焉》.txt"
# s3_client.upload_file(new_file_path, bucket_name, object_key)
# print(f'Object {object_key} in {bucket_name} updated.')
# print("+---------------------------------+")
# # 获取特定存储桶中的对象列表
# bucket_name = 'my-new-bucket'
# response = s3_client.list_objects_v2(Bucket=bucket_name)
# objects = response.get('Contents', [])
# print(f'Objects in bucket {bucket_name}:')
# for obj in objects:
#     print(obj['Key'])
# print("+---------------------------------+")
# 删除存储桶中的一个对象

object_key = '《深空彼岸》.txt'
s3_client.delete_object(Bucket=bucket_name, Key=object_key)
print(f'Object {object_key} deleted from {bucket_name}.')
print("+---------------------------------+")
# 删除一个对象之后，重新获取特定存储桶中的对象列表
# 获取特定存储桶中的对象列表

response = s3_client.list_objects_v2(Bucket=bucket_name)
objects = response.get('Contents', [])
print(f'Objects in bucket {bucket_name}:')
for obj in objects:
    print(obj['Key'])
print("+---------------------------------+")
# 删除存储桶（注意：这将删除存储桶中的所有对象）
s3_client.delete_bucket(Bucket=bucket_name)
print(f'Bucket {bucket_name} deleted.')