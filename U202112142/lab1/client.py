from swiftclient import client

# 设置你的认证信息
auth_url = 'http://127.0.0.1:12345/auth/v1.0'
auth_username = 'chris:chris1234'
auth_password = 'testing'

# 获取认证
conn = client.Connection(
    authurl=auth_url,
    user=auth_username,
    key=auth_password,
    auth_version='1.0'
)

# 创建一个 bucket (在 Swift 中，这通常被称为 container)
container_name = 'my_new_container'
conn.put_container(container_name)

# 上传一个文件 (Create)
object_name = 'my_object'
with open('./anypdf.pdf', 'rb') as file:
    conn.put_object(container_name, object_name, contents=file.read())

# 读取一个文件 (Read)
response_headers, file_contents = conn.get_object(container_name, object_name)
print(file_contents)

# 更新一个文件 (Update)
# 在 Swift 中，更新一个对象通常意味着完全替换它
object_name = 'my_object'
with open('./anypdf2.pdf', 'rb') as file:
    conn.put_object(container_name, object_name, contents=file.read())

# 删除一个文件 (Delete)
conn.delete_object(container_name, object_name)

# 删除一个 bucket
conn.delete_container(container_name)
