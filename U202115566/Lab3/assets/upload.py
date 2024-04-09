import boto3
import os
import threading
import matplotlib.pyplot as plt
import time

# 初始化 S3 客户端
s3 = boto3.client(
    's3',
    endpoint_url='http://127.0.0.1:8080'
)


# 创建指定大小的文件
def create_file(file_path, size_in_bytes):
    with open(file_path, 'wb') as f:
        f.write(b'\0' * size_in_bytes)


# 测试上传文件的性能
def test_upload(bucket_name, file_path, object_key, upload_times, latencies):
    start_time = time.time()
    s3.upload_file(file_path, bucket_name, object_key)
    end_time = time.time()
    upload_time = end_time - start_time
    upload_times.append(upload_time)
    # 计算延迟
    latency = upload_time
    latencies.append(latency)


# 模拟并发上传
def concurrent_upload(bucket_name, file_path, object_key, num_threads):
    upload_times = []
    latencies = []
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=test_upload, args=(bucket_name, file_path, object_key, upload_times, latencies))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # 计算吞吐率
    total_time = sum(upload_times)
    total_data_size = os.path.getsize(file_path) * num_threads
    throughput = total_data_size / total_time

    # 计算效率
    efficiency = throughput * num_threads

    return throughput, efficiency, latencies


if __name__ == "__main__":
    bucket_name = 'test'
    object_key = 'test_object'
    desired_size_in_bytes = 1024 * 1024  # 1 MB

    # 创建指定大小的文件
    temp_file_path = 'temp_file.txt'
    create_file(temp_file_path, desired_size_in_bytes)

    num_threads_list = list(range(10, 500, 10))  # 并发数列表

    throughputs = []  # 存储吞吐率
    avg_latencies = []  # 存储平均延迟
    efficiencies = []  # 存储效率
    for num_threads in num_threads_list:
        # 测试并发上传
        throughput, efficiency, latencies = concurrent_upload(bucket_name, temp_file_path, object_key, num_threads)
        throughputs.append(throughput / (1024 * 1024))  # 将吞吐率转换为 MB/second
        avg_latency = sum(latencies) / len(latencies)
        avg_latencies.append(avg_latency)
        efficiencies.append(efficiency/(1024*1024))
    # 输出吞吐率和平均延迟
    for i, num_threads in enumerate(num_threads_list):
        print(
            f"Concurrency: {num_threads}, Throughput: {throughputs[i]:.2f} MB/second, Average Latency: {avg_latencies[i]:.2f} seconds")

    # 绘制图表
    plt.plot(num_threads_list, throughputs)
    plt.xlabel('Concurrency')
    plt.ylabel('Throughput (MB/second)')
    plt.title('Throughput vs Concurrency')
    plt.grid(True)
    plt.show()
    # 绘制图表
    plt.plot(num_threads_list, efficiencies)
    plt.xlabel('Concurrency')
    plt.ylabel('Actual processing capacity (MB/second)')
    plt.title('Actual processing capacity vs Concurrency')
    plt.grid(True)
    plt.show()
    # 绘制图表
    plt.plot(num_threads_list, avg_latencies)
    plt.xlabel('Concurrency')
    plt.ylabel('Average Latency (seconds)')
    plt.title('Average Latency vs Concurrency')
    plt.grid(True)
    plt.show()
    # 删除临时文件
    os.remove(temp_file_path)
