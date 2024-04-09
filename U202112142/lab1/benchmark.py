from swiftclient import client
import timeit

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

# 创建一个 bucket
container_name = 'my_new_container'
conn.put_container(container_name)

# 测试数据
object_name = 'my_object'
test_data = b'This is some test data'

# 定义测试函数
def test_operations():
    conn.put_object(container_name, object_name, contents=test_data)
    _, _ = conn.get_object(container_name, object_name)
    conn.put_object(container_name, object_name, contents=test_data)
    conn.delete_object(container_name, object_name)

# 测试次数
num_tests = 100

# 执行测试并计算平均时间
total_time = timeit.timeit(test_operations, number=num_tests) / num_tests

# 输出结果
print(f'Average time for CRUD operations: {total_time} seconds')

# 删除测试用的 bucket
conn.delete_container(container_name)
