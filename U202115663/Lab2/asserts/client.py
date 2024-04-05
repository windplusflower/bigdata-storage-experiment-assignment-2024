# -*- coding: utf-8 -*-
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import current_thread
from tqdm import tqdm
import swiftclient
import matplotlib.pyplot as plt

# 定义上传对象的函数
def bench_put(i):
    """
    上传对象至 Swift 存储的函数。

    Args:
        i (int): 正在上传对象的索引。

    Returns:
        tuple: 包含操作持续时间、开始时间、结束时间和客户端名称的元组。
    """
    obj_name = f"{object_name_prefix}{i:08d}"  # 生成对象名称
    start = time.time()
    with open(local_file, 'rb') as f:
        conn.put_object(bucket_name, obj_name, f)  # 上传文件对象
    end = time.time()
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)

# 定义获取对象的函数
def bench_get(i):
    """
    从 Swift 存储检索对象的函数。

    Args:
        i (int): 正在检索对象的索引。

    Returns:
        tuple: 包含操作持续时间、开始时间、结束时间和客户端名称的元组。
    """
    obj_name = f"{object_name_prefix}{i:08d}"  # 生成对象名称
    start = time.time()
    resp_headers, obj_contents = conn.get_object(bucket_name, obj_name)
    with open(obj_name, 'wb') as f:
        f.write(obj_contents)
    end = time.time()
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)

# 定义删除对象的函数
def bench_delete(i):
    """
    从 Swift 存储中删除对象的函数。

    Args:
        i (int): 正在删除对象的索引。

    Returns:
        tuple: 包含操作持续时间、开始时间、结束时间和客户端名称的元组。
    """
    obj_name = f"{object_name_prefix}{i:08d}"  # 生成对象名称
    start = time.time()
    conn.delete_object(bucket_name, obj_name)
    end = time.time()
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)

# 定义更新对象的函数
def bench_update(i):
    """
    更新 Swift 存储中对象的函数。

    Args:
        i (int): 正在更新对象的索引。

    Returns:
        tuple: 包含操作持续时间、开始时间、结束时间和客户端名称的元组。
    """
    obj_name = f"{object_name_prefix}{i:08d}"  # 生成对象名称
    start = time.time()
    
    # 更新对象
    with open(local_file, 'rb') as f:
        conn.put_object(bucket_name, obj_name, f)

    # # 重新读取对象
    # resp_headers, obj_contents = conn.get_object(bucket_name, obj_name)
    # with open(obj_name, 'wb') as f:
    #     f.write(obj_contents)
        
    end = time.time()
    duration = end - start
    client = current_thread().name
    return (duration, start, end, client)

# 字典，将操作类型映射到相应的函数
switch = {'write': bench_put, 'read': bench_get, 'delete': bench_delete, 'update': bench_update}

# 运行特定操作类型测试的函数
def run_test(test_type):
    """
    运行指定操作类型的测试。

    Args:
        test_type (str): 操作类型（'write'、'read'、'update' 或 'delete'）。
    """
    print('-----' + test_type + '-----')
    latency = []
    failed_requests = []
    test_start_time = time.time()
    with tqdm(desc="Accessing S3", total=num_samples) as pbar:
        with ThreadPoolExecutor(max_workers=num_client) as executor:
            futures = [executor.submit(switch[test_type], i) for i in range(num_samples)]
            for future in as_completed(futures):
                if future.exception():
                    failed_requests.append(future)
                else:
                    latency.append(future.result())  # 记录成功的请求
                pbar.update(1)
    test_end_time = time.time()
    test_duration = test_end_time - test_start_time # 测试持续时间（秒）
    test_transferred = len(latency) * object_size # 总数据传输量（KB）
    test_total_throughput = test_transferred / test_duration # 总吞吐量（KB/s）
    test_average_latency = sum([latency[i][0] for i in range(len(latency))]) / len(latency) # 平均延迟（秒）
    print('总持续时间：', test_duration , '秒')
    print('平均延迟：', test_average_latency,"秒")
    print('总传输量：', test_transferred , 'KB')
    print('总吞吐量：', test_transferred / test_duration, 'KB/s')
    print('成功率：', len(latency) / num_samples * 100, '%')

    # 将结果写入文件
    with open(result_file, "a") as rf:
        rf.write("num_client: " + str(num_client) + " \n")
        rf.write(f"{test_type}_total_throughput: {test_total_throughput} KB/s\n")
        rf.write(f"{test_type}_average_latency: {test_average_latency} 秒\n")

# Swift 存储的端点和凭据
endpoint = 'http://127.0.0.1:12345/'
_user_ = 'test:tester'
_key_ = 'testing'
# bucket_name 是 Swift 中的容器名
bucket_name = 'testbucket' 
object_name_prefix = 'testObj'
total_size = 4 * 1024 # 总大小（KB）
object_size = 8 # 对象大小（KB）
num_samples = 1024 # 样本数
num_clients = list(range(1, 20, 2)) + list(range(20, 200, 20)) # 客户端数
result_file = "result.txt" # 存储结果的文件

print('端点：', endpoint)
print('容器名：', bucket_name)
print('对象前缀：', object_name_prefix)
print("总大小：", total_size, "KB")
print("对象大小：", object_size, "KB")
print("样本数：", num_samples)

# 如果结果文件存在，则删除
if os.path.exists(result_file):
    os.remove(result_file)

# 连接到 Swift 存储
conn = swiftclient.Connection(authurl=endpoint + 'auth/v1.0', user=_user_, key=_key_)

# 遍历不同数量的客户端
for num_client in num_clients:
    print("=====测试=====")
    print("客户端数:", num_client)
    
    # 创建一个新容器
    conn.put_container(bucket_name)
    print('已创建测试容器 %s。' % bucket_name)

    # 初始化指定大小的文件
    local_file = "_test.bin"
    test_bytes = [0xFF for i in range(object_size * 1024)]
    with open(local_file, "wb") as lf:
        lf.write(bytearray(test_bytes))
    print('已创建测试文件 %s。' % local_file)

    # 运行写入、读取、更新并重新读取、删除操作的测试
    run_test('write')
    run_test('read')
    run_test('update')
    run_test('delete')

    # 删除下载的文件
    for i in range(num_samples):
        obj_name = f"{object_name_prefix}{i:08d}"
        os.remove(obj_name)
    print('已删除下载的文件。')

    # 删除测试文件
    os.remove(local_file)
    print('已删除测试文件 %s。' % local_file)

    # 删除容器
    conn.delete_container(bucket_name)
    print('已删除测试容器 %s。' % bucket_name)

# 处理结果文件并绘图
write_throughputs = []
write_latencies = []
read_throughputs = []
read_latencies = []
update_throughputs = []
update_latencies = []

# Parse the result file
with open(result_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        if line.startswith('write_total_throughput'):
            write_throughputs.append(float(line.split(':')[1].strip().split()[0]))
        elif line.startswith('write_average_latency'):
            write_latencies.append(float(line.split(':')[1].strip().split()[0]))
        elif line.startswith('read_total_throughput'):
            read_throughputs.append(float(line.split(':')[1].strip().split()[0]))
        elif line.startswith('read_average_latency'):
            read_latencies.append(float(line.split(':')[1].strip().split()[0]))
        elif line.startswith('update_total_throughput'):
            update_throughputs.append(float(line.split(':')[1].strip().split()[0]))
        elif line.startswith('update_average_latency'):
            update_latencies.append(float(line.split(':')[1].strip().split()[0]))

    # Plotting
    # Write throughput plot
    plt.figure(figsize=(8, 6))
    plt.plot(num_clients, write_throughputs, marker='o',color='blue', label='Write Throughput')
    plt.xlabel('Number of Clients')
    plt.ylabel('Throughput (KB/s)')
    plt.title('Write Throughput')
    plt.grid(True)
    plt.legend()
    plt.savefig('write_throughputs.png')
    plt.show()

    # Read throughput plot
    plt.figure(figsize=(8, 6))
    plt.plot(num_clients, read_throughputs, marker='o', color='orange', label='Read Throughput')
    plt.xlabel('Number of Clients')
    plt.ylabel('Throughput (KB/s)')
    plt.title('Read Throughput')
    plt.grid(True)
    plt.legend()
    plt.savefig('read_throughputs.png')
    plt.show()

    # Update throughput plot
    plt.figure(figsize=(8, 6))
    plt.plot(num_clients, update_throughputs, marker='o', color='green', label='Update Throughput')
    plt.xlabel('Number of Clients')
    plt.ylabel('Throughput (KB/s)')
    plt.title('Update Throughput')
    plt.grid(True)
    plt.legend()
    plt.savefig('update_throughput.png')
    plt.show()
