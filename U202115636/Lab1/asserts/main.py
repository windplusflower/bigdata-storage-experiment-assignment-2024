import boto3

boto3.set_stream_logger("botocore", level="ERROR")

session = boto3.session.Session()
s3_client = session.client(
    service_name="s3",
    endpoint_url="http://localhost:7480",
)

# create bucket
s3_client.create_bucket(Bucket="mybucket")

# list all buckets
response = s3_client.list_buckets()
print("Existing buckets:")
for bucket in response["Buckets"]:
    print(f"  {bucket['Name']}")


# put object
s3_client.put_object(Bucket="mybucket", Key="hello.txt", Body="Hello World")

# list objects
response = s3_client.list_objects(Bucket="mybucket")
print("Existing objects in mybucket:")
for obj in response["Contents"]:
    print(f"  {obj['Key']}")

# get object
response = s3_client.get_object(Bucket="mybucket", Key="hello.txt")
print("Content of hello.txt:")
print(response["Body"].read().decode("utf-8"))


# update object
s3_client.put_object(Bucket="mybucket", Key="hello.txt", Body="Hello World Updated")

# get object
response = s3_client.get_object(Bucket="mybucket", Key="hello.txt")
print("Content of hello.txt:")
print(response["Body"].read().decode("utf-8"))

# delete object
s3_client.delete_object(Bucket="mybucket", Key="hello.txt")

# list objects
response = s3_client.list_objects(Bucket="mybucket")

if "Contents" not in response:
    print("no objects found in mybucket")
else:
    print("Existing objects in mybucket:")
    for obj in response["Contents"]:
        print(f"  {obj['Key']}")
        
# delete bucket
s3_client.delete_bucket(Bucket="mybucket")

