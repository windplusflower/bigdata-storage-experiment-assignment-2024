import boto3

s3 = boto3.client(
    's3',
    endpoint_url='http://127.0.0.1:8080'
)


def create_object(bucket_name, file_path, object_key):
    # 上传文件到存储桶
    with open(file_path, 'rb') as file:
        s3.upload_fileobj(file, bucket_name, object_key)

    print("Object uploaded successfully.")


def read_object(bucket_name, object_key):
    # 获取对象内容
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    object_data = response['Body'].read().decode('utf-8')

    print("Object Content:")
    print(object_data)


def update_object(bucket_name, new_file_path, object_key):
    # 上传新文件替换原有对象
    with open(new_file_path, 'rb') as file:
        s3.upload_fileobj(file, bucket_name, object_key)

    print("Object updated successfully.")


def delete_object(bucket_name, object_key):
    # 删除对象
    s3.delete_object(Bucket=bucket_name, Key=object_key)

    print("Object deleted successfully.")


# 测试
if __name__ == "__main__":
    bucket_name = 'test'
    file_path = 'test.txt'
    object_key = 'test.txt'
    new_file_path = 'new.txt'

    # 上传对象
    create_object(bucket_name, file_path, object_key)

    # 读取对象
    read_object(bucket_name, object_key)

    # 更新对象
    update_object(bucket_name, new_file_path, object_key)

    # 读取更新后的对象
    read_object(bucket_name, object_key)

    # 删除对象
    delete_object(bucket_name, object_key)
