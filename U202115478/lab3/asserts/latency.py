import swiftclient
import time
from swiftclient import Connection
from typing import List, Callable, Dict
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor


endpoint: str = "http://127.0.0.1:12345/auth/v1.0"
user: str = "test:tester"
key: str = "testing"
bucket_name: str = "TestBucket"
obj_name_prefix: str = "TestObj"
obj_count: int = 0
client_num: List[int] = [4, 8, 16, 32, 64, 128, 256]


def init():
    conn: Connection = swiftclient.Connection(
        authurl=endpoint, user=user, key=key)
    conn.put_container(bucket_name)
    conn.close()


def put_bench(num: int):
    conn: Connection = swiftclient.Connection(
        authurl=endpoint, user=user, key=key)
    start_time: float = time.time()
    with open("test.txt", "rb") as f:
        conn.put_object(bucket_name, obj_name_prefix + str(num), f)
    total_time: float = time.time() - start_time
    conn.close()
    return total_time


def get_bench(num: int):
    conn: Connection = swiftclient.Connection(
        authurl=endpoint, user=user, key=key)
    start_time: float = time.time()
    _, _ = conn.get_object(bucket_name, obj_name_prefix + str(num))
    total_time: float = time.time() - start_time
    conn.close()
    return total_time


def __list_objects(conn: Connection) -> List[str]:
    _, objects = conn.get_container(bucket_name)
    objs: List[str] = []
    for obj in objects:
        objs.append(obj['name'])
    return objs


def clear():
    conn: Connection = swiftclient.Connection(
        authurl=endpoint, user=user, key=key)
    remain_objs = __list_objects(conn)
    if len(remain_objs) != 0:
        for obj in remain_objs:
            conn.delete_object(bucket_name, obj)
    conn.delete_container(bucket_name)
    conn.close()


name2test: Dict[str, Callable] = {'put': put_bench, 'get': get_bench}


def run_test(test: str):
    print(f"Running {test} bench test...")

    latency: List[Queue] = [Queue(i) for i in client_num]
    count: int = 0
    test_start_time = time.time()
    for (batch, num) in enumerate(client_num):
        with ThreadPoolExecutor(max_workers=num) as executor:
            futures = [executor.submit(name2test[test], i)
                       for i in range(count, count+num)]
            count = count+num

            for future in as_completed(futures):
                if future.exception():
                    print(future.exception())
                else:
                    latency[batch].put(future.result())

    test_end_time = time.time()

    print(f"{test} bench test use time: {(test_end_time-test_start_time):.2f}s")

    average_latency: List[float] = [
        sum(list(latency[i].queue))/len(latency[i].queue) for i in range(len(client_num))]
    throughput: List[float] = [
        4*num/total_time for (total_time, num) in zip(average_latency, client_num)]

    file_name = f"{test}_test.txt"

    print(f"start to write test data to {file_name}")

    with open(file_name, "w+") as f:
        f.write(f"id,client_num,average_latency,throughput\n")
        for i in range(len(client_num)):
            f.write(
                f'{i},{client_num[i]},{average_latency[i]:.4f},{throughput[i]:.4f}\n')

    print(f"{test} bench finished")


def main():
    init()
    run_test("put")
    run_test("get")
    print("all tests finished")
    clear()


if __name__ == "__main__":
    main()
