import boto3

# 修改Access Key和Secret Key
access_key = '8XUw990Grl7L6JcBeG7l'
secret_key = '5rhdPHmVKwOXi0AVCGrJ0t6GUpLlP00KRqrHGYX1'

# 修改为Minio Server正在运行的网址
endpoint_url = 'http://127.0.0.1:9000'

s3 = boto3.client('s3',
                  endpoint_url=endpoint_url,
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key)

"""桶操作"""
# 创建桶
def create_bucket(bucket_name):
    s3.create_bucket(Bucket=bucket_name)
    print(f'Bucket {bucket_name} created.\n')

# 列出所有桶
def list_buckets():
    response = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return buckets

# 更新桶内对象
def update_object(bucket_name, object_key, new_file_path):
    # 重新上传对象以更新其内容
    with open(new_file_path, "rb") as f:
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=f)
    
    print(f"Object '{object_key}' in bucket '{bucket_name}' updated.\n")

# 删除桶
def delete_bucket(bucket_name):
    s3.delete_bucket(Bucket=bucket_name)
    print(f'Bucket {bucket_name} deleted.\n')

"""对象操作"""
# 上传对象
def upload_object(bucket_name, object_key, file_path):
    s3.upload_file(file_path, bucket_name, object_key)
    print(f"Object '{object_key}' from '{file_path}' uploaded to bucket '{bucket_name}'\n")

# 下载对象
def download_object(bucket_name, object_key, local_file_path):
    s3.download_file(bucket_name, object_key, local_file_path)
    print(f"Object '{object_key}' downloaded from bucket '{bucket_name}' to Local '{local_file_path}'\n")

# 桶内互相拷贝对象
def copy_object(source_bucket, source_key, dest_bucket, dest_key):
    s3.copy_object(Bucket=dest_bucket, Key=dest_key, CopySource={'Bucket': source_bucket, 'Key': source_key})
    print(f"Object '{object_key}' copied from bucket '{source_bucket}' to bucket '{dest_bucket}'\n")

# 删除桶内对象
def delete_object(bucket_name, object_key):
    s3.delete_object(Bucket=bucket_name, Key=object_key)
    print(f"Object '{object_key}' deleted from bucket '{bucket_name}'\n")

# 用户选择操作
while True:
    print("1. Create Bucket")
    print("2. Read Bucket(List Bucket)")
    print("3. Update Object in Bucket")
    print("4. Delete Bucket")
    print("5. Upload Object")
    print("6. Download Object")
    print("7. Copy Object")
    print("8. Delete Object")
    print("0. Exit")
    choice = input("Please KeyIn 0~8: ")

    if choice == "1":
        print("\nCreating Bucket")
        bucket_name = input("Bucket Name: ")
        create_bucket(bucket_name)

    elif choice == "2":
        print("\nListing Bucket")
        buckets = list_buckets()
        print("Bucket List:")
        for bucket in buckets:
            print(bucket)
            print()

    elif choice == "3":
        print("\nUpdating Object in Bucket")
        bucket_name = input("Bucket Name: ")
        object_key = input("Object Name: ")
        new_file_path = input("New File Path: ")
        update_object(bucket_name, object_key, new_file_path)

    elif choice == "4":
        print("\nDeleting Bucket")
        bucket_name = input("Bucket Name: ")
        delete_bucket(bucket_name)

    elif choice == "5":
        print("\nUploading New Object to Bucket")
        bucket_name = input("Bucket Name: ")
        object_key = input("Object Key: ")
        file_path = input("File Path: ")
        upload_object(bucket_name, object_key, file_path)

    elif choice == "6":
        print("\nDownloading Object from Bucket")
        bucket_name = input("Bucket Name: ")
        object_key = input("Object Key: ")
        local_file_path = input("Local File Path: ")
        download_object(bucket_name, object_key, local_file_path)

    elif choice == "7":
        print("\nCopying Object from Bucket to Bucket")
        source_bucket = input("Source Bucket Name: ") 
        source_key = input("Source Object Key: ")
        dest_bucket = input("Destination Bucket Name: ")
        dest_key = input("Destination Object Key: ")
        copy_object(source_bucket, source_key, dest_bucket, dest_key)

    elif choice == "8":
        print("Deleting Object in Bucket")
        bucket_name = input("Bucket Name: ")
        object_key = input("Object Key: ")
        delete_object(bucket_name, object_key)

    elif choice == "0":
        print("Thanks for using! See you Next Time!")
        break
    
    else:
        print("Invalid Number! Please try again!")