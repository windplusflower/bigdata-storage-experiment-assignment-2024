import random
import swiftclient
import time
import threading
from swiftclient import Connection
from typing import List, Callable
from threading import Thread

endpoint: str = "http://127.0.0.1:12345/auth/v1.0"
user: str = "test:tester"
key: str = "testing"
containers: List[str] = ["c1", "c2", "c3", "c4"]
objects: List[str] = ["test.txt", "big.txt"]
object_num: int = 0
base_size: int = 100  # 100MB


def connect() -> Connection:
    return swiftclient.Connection(
        authurl=endpoint, user=user, key=key)


def create_container(conn: Connection, name: str) -> None:
    conn.put_container(name)


def clear(conn: Connection, name: str) -> None:
    remain_objs = __list_objects(conn, name)
    if len(remain_objs) != 0:
        for obj in remain_objs:
            conn.delete_object(name, obj)
    conn.delete_container(name)


def put_objects(conn: Connection, name: str) -> None:
    global object_num
    num: int = random.randint(2, 5)
    size: int = 0
    start: float = time.time()
    for i in range(num):
        object_num += 1
        filename: str = f"obj{object_num}"
        file_index: int = random.randint(0, 1)
        file = objects[file_index]
        size += base_size * (file_index+1)
        with open(file, "rb") as f:
            conn.put_object(name, filename, f)
    end = time.time()
    print(f"put {size}MB files to container {name},using {(end-start):.2f}s,write speed {((size)/(end-start)):.2f}MB/s")


def list_objects(conn: Connection, name: str) -> None:
    _, objects = conn.get_container(name)
    objs: List[str] = __list_objects(conn, name)
    print(f"container {name} has {len(objects)} objects: {objs}")


def __list_objects(conn: Connection, name: str) -> List[str]:
    _, objects = conn.get_container(name)
    objs: List[str] = []
    for obj in objects:
        objs.append(obj['name'])
    return objs


def __read_objects(conn: Connection, name: str, obj_name: str, start_byte: int, end_byte: int) -> bytes:
    _, obj_contents = conn.get_object(
        name, obj_name, headers={'Range': 'bytes={}-{}'.format(start_byte, end_byte)})
    return obj_contents


def __read_all_objects(conn: Connection, name: str, obj_name: str) -> bytes:
    _, obj_contents = conn.get_object(
        name, obj_name)
    return obj_contents


def read_objects(conn: Connection, name: str) -> None:
    start_byte: int = 0
    total_bytes: int = 0
    objs: List[str] = __list_objects(conn, name)
    start_time: float = time.time()
    for obj in objs:
        obj_size: int = random.randint(1, 100) * 1024*1024
        total_bytes += obj_size
        __read_objects(
            conn, name, obj, start_byte, obj_size)
    end_time: float = time.time()
    total: int = total_bytes/1024/1024
    print(
        f"read {total}MB contents from container {name} using {(end_time-start_time):.2f}s ,read speed= {(total/(end_time-start_time)):.2f}MB/s")


def update_objects(conn: Connection, name: str) -> None:
    objs: List[str] = __list_objects(conn, name)
    size: int = 0
    start_time = time.time()
    for obj in objs:
        contents: bytes = __read_all_objects(conn, name, obj)
        size += len(contents)/1024/1024
        contents: bytes = contents.upper()
        conn.put_object(name, obj, contents)
    end_time = time.time()
    print(
        f"update {size}MB contents from container {name} using {(end_time-start_time):.2f}s ,update speed= {(size/(end_time-start_time)):.2f}MB/s")


def apply_to_all(func: Callable, conn: Connection) -> None:
    for name in containers:
        func(conn, name)


def thread_main(conn: Connection, name: str):
    create_container(conn, name)
    put_objects(conn, name)
    # list_objects(conn, name)
    read_objects(conn, name)
    update_objects(conn, name)
    clear(conn, name)


def main_with_threads() -> None:
    print("4 threads main start!")
    start_time = time.time()
    conn: Connection = connect()
    threads: List[Thread] = []
    for name in containers:
        thread: Thread = threading.Thread(
            target=thread_main, args=(conn, name))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    conn.close()
    end_time = time.time()
    print(f"4 threads op CURD using {(end_time-start_time):.2f}s\n")


def main():
    print("single thread main start!")
    start_time = time.time()

    conn: Connection = connect()
    apply_to_all(create_container, conn)
    apply_to_all(put_objects, conn)
    # apply_to_all(list_objects, conn)
    apply_to_all(read_objects, conn)
    apply_to_all(update_objects, conn)
    apply_to_all(clear, conn)
    conn.close()

    end_time = time.time()
    print(f"single thread op CURD using {(end_time-start_time):.2f}s")


if __name__ == "__main__":
    main_with_threads()
    main()
