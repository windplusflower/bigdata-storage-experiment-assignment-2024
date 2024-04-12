import os
import time
import swiftclient
import matplotlib.pyplot as plt

# 创建
def create_file(object_name_prefix, bucket_name, local_file, conn, num_samples):
    for i in range(num_samples):
        obj_name = '%s%08d' % (object_name_prefix, i)
        with open(local_file, 'rb') as f:
            conn.put_object(bucket_name, obj_name, f)

# 读取
def read_file(object_name_prefix, bucket_name, conn, num_samples):
    for i in range(num_samples):
        obj_name = '%s%08d' % (object_name_prefix, i)
        resp_headers, obj_contents = conn.get_object(bucket_name, obj_name)
        with open(obj_name, 'wb') as f:
            f.write(obj_contents)

# 删除
def delete_file(object_name_prefix, bucket_name, conn, num_samples):
    for i in range(num_samples):
        obj_name = '%s%08d' % (object_name_prefix, i)
        conn.delete_object(bucket_name, obj_name)

# 测试函数
def run_test(test_type, object_name_prefix, bucket_name, local_file, conn, num_samples):
    print('-----' + test_type + '-----')
    test_start_time = time.time()

    if test_type == 'create':
        create_file(object_name_prefix, bucket_name, local_file, conn, num_samples)
    elif test_type == 'read':
        read_file(object_name_prefix, bucket_name, conn, num_samples)
    elif test_type == 'delete':
        delete_file(object_name_prefix, bucket_name, conn, num_samples)

    test_end_time = time.time()
    test_duration = test_end_time - test_start_time
    throughput = 4096 / test_duration
    print('总时间:', test_duration, 's')
    print('吞吐率:', throughput, 'KB/s')
    return throughput

# 初始化
auth_url = 'http://127.0.0.1:12345/auth/v1.0'
user = 'test:tester'
key = 'testing'
bucket_name = 'first_try'
object_name_prefix = 'testobj'
object_sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]  # KB
total_size = 4 * 1024  # 4MB

# 连接
conn = swiftclient.Connection(authurl=auth_url, user=user, key=key)

# 测试不同尺寸但都是4MB大小数据所需时间
throughput_write = []
throughput_read = []
throughput_delete = []

for object_size in object_sizes:
    print("=====TEST=====")
    print("object_size:", object_size, "KB")
    local_file = f"_test_{object_size}.bin"
    test_bytes = [0xFF for i in range(object_size * 1024)]
    with open(local_file, "wb") as lf:
        lf.write(bytearray(test_bytes))
    print('Test file %s created.' % local_file)
    num_samples = int(4096/object_size)
    throughput_write.append(run_test('create', object_name_prefix, bucket_name, local_file, conn, num_samples))
    throughput_read.append(run_test('read', object_name_prefix, bucket_name, local_file, conn, num_samples))
    throughput_delete.append(run_test('delete', object_name_prefix, bucket_name, local_file, conn, num_samples))

    # 删除本地文件
    for i in range(num_samples):
        obj_name = '%s%08d' % (object_name_prefix, i)
        os.remove(obj_name)
    print('Downloaded files deleted.')

    # 删除数据文件
    os.remove(local_file)
    print('Test file %s deleted.' % local_file)

print(throughput_write)
print(throughput_read)
print(throughput_delete)

plt.plot(object_sizes, throughput_write, label='write', marker='.', markersize=10)
plt.plot(object_sizes, throughput_read, label='read', marker='.', markersize=10)
plt.plot(object_sizes, throughput_delete, label='delete', marker='.', markersize=10)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.title('吞吐率随文件大小变化图')
plt.xlabel('每个文件的大小 /KB')
plt.ylabel('吞吐率/ KB/s')

plt.legend()
plt.show()




