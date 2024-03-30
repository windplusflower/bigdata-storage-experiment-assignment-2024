from swiftclient import client

# OpenStack Swift服务端点URL
auth_url = 'http://127.0.0.1:12345/auth/v1.0' 
username = 'chris:chris1234'
api_key = 'testing'

# 连接Swift服务
conn = client.Connection(authurl=auth_url, user=username, key=api_key)

def list_all():
    """
    列出所有对象
    """
    containers = conn.get_account()[1]
    # 遍历每个容器，并列出其中的对象
    print("********list_all*********")
    for container in containers:
        container_name = container['name']
        
        # 列出容器内的所有对象
        objects = conn.get_container(container_name)[1]
        print(f"{container_name}:")
        for obj in objects:
            object_name = obj['name']
            print(f"\t{object_name}")
            
    print("********  end  *********\n\n")

# 列出所有容器
list_all()



# 定义要创建的容器名称
container_name = 'my-container'
# 创建容器
conn.put_container(container_name)
print(f"Container '{container_name}' created.")
list_all()
    


# 定义本地文件路径和上传到容器后的对象名称
local_file_path = './swifttest.txt'
object_name = 'test.txt'
# 上传文件到容器
with open(local_file_path, 'rb') as file_to_upload:
    conn.put_object(container_name, object_name, contents=file_to_upload.read())
print(f"File '{local_file_path}' uploaded to container '{container_name}' as '{object_name}'.")
list_all()



# 下载对象
remote_object_name = 'test.txt'
destination_file_path = './test.txt'
_, contents = conn.get_object(container_name, remote_object_name)
with open(destination_file_path, 'wb') as downloaded_file:
    downloaded_file.write(contents)
print(f"File '{remote_object_name}' from container '{container_name}' downloaded to '{destination_file_path}'.")
list_all()



#删除对象
conn.delete_object(container_name, object_name)
print(f"The request to delete objective '{object_name}' has been sent.")
list_all()



# 删除容器
headers = {}
conn.delete_container(container_name, headers=headers)
print(f"The request to delete container '{container_name}' has been sent.")
list_all()



# 关闭连接
conn.close()