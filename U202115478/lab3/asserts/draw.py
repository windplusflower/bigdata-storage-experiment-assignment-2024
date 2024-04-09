from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


def get_data(filename: str) -> Tuple[List[int], List[float], List[float]]:
    client_num: List[int] = []
    latency: List[float] = []
    throughput: List[float] = []
    with open(filename, "r") as f:
        lines: List[str] = f.readlines()[1:]
        for line in lines:
            nums = line.strip('\n').split(',')
            client_num.append(int(nums[1]))
            latency.append(float(nums[2]))
            throughput.append(float(nums[3]))
    return client_num, latency, throughput


def __draw(x: List[int], y: List[float], title: str, xlabel: str, ylabel: str, xticks, yticks):
    plt.plot(x, y, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xticks is not None:
        plt.xticks(xticks)
    if yticks is not None:
        plt.yticks(yticks)
    plt.show()


def draw(filename: str):
    client_num, latency, throughput = get_data(filename)
    test: str = "Put" if "put" in filename else "Get"

    __draw(client_num, latency, f'{test} Latency Vs Client Number', 'Client Number', 'Latency', client_num,
           np.arange(round(min(latency), 1), round(max(latency), 1) + 0.1, 0.1))

    __draw(client_num, throughput, f'{test} Throughput Vs Client Number', 'Client NUmber', 'Throughput (MB/S)',
           client_num, np.arange(round(min(throughput)), round(max(throughput)) + 20, 20))


def main():
    put_test_name: str = "put_test.txt"
    get_test_name: str = "get_test.txt"
    draw(put_test_name)
    draw(get_test_name)


if __name__ == '__main__':
    main()
