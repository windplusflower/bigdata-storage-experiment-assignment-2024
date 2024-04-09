import matplotlib.pyplot as plt
import os
import re
import json


def parse_text_to_json(text):
    # 使用正则表达式提取信息
    object_size = float(re.search(r'objectSize:\s+(\d+\.\d+)', text).group(1))
    num_clients = int(re.search(r'numClients:\s+(\d+)', text).group(1))

    write_info = re.search(
        r'Results Summary for Write Operation\(s\)(.*?)\n\n', text, re.DOTALL).group(1)
    read_info = re.search(
        r'Results Summary for Read Operation\(s\)(.*?)\n\n', text, re.DOTALL).group(1)

    write_dict = {
        'Total Transferred': float(re.search(r'Total Transferred:\s+(\d+\.\d+)', write_info).group(1)),
        'Total Throughput': float(re.search(r'Total Throughput:\s+(\d+\.\d+)', write_info).group(1)),
        'Total Duration': float(re.search(r'Total Duration:\s+(\d+\.\d+)', write_info).group(1)),
        'Write times Max': float(re.search(r'Write times Max:\s+(\d+\.\d+)', write_info).group(1)),
        'Write times 99th %ile': float(re.search(r'Write times 99th %ile:\s+(\d+\.\d+)', write_info).group(1)),
        'Write times Min': float(re.search(r'Write times Min:\s+(\d+\.\d+)', write_info).group(1))
    }

    read_dict = {
        'Total Transferred': float(re.search(r'Total Transferred:\s+(\d+\.\d+)', read_info).group(1)),
        'Total Throughput': float(re.search(r'Total Throughput:\s+(\d+\.\d+)', read_info).group(1)),
        'Total Duration': float(re.search(r'Total Duration:\s+(\d+\.\d+)', read_info).group(1)),
        'Read times Max': float(re.search(r'Read times Max:\s+(\d+\.\d+)', read_info).group(1)),
        'Read times 99th %ile': float(re.search(r'Read times 99th %ile:\s+(\d+\.\d+)', read_info).group(1)),
        'Read times Min': float(re.search(r'Read times Min:\s+(\d+\.\d+)', read_info).group(1))
    }

    # 将信息存储在字典中
    data = {
        'objectSize': object_size,
        'numClients': num_clients,
        'write': write_dict,
        'read': read_dict
    }

    # 将字典转换为JSON格式
    json_data = json.dumps(data, indent=2)

    return json_data


# 文件名列表
file_names = ['numClients2.txt', 'numClients4.txt',
              'numClients6.txt', 'numClients8.txt', 'numClients10.txt']

# 初始化一个空列表来存储所有的数据
all_data = []

for file_name in file_names:
    file_path = os.path.join(os.path.dirname(__file__), 'output', file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        text_input = file.read()

    # 解析文本并生成JSON对象
    json_object = parse_text_to_json(text_input)

    # 将JSON对象添加到all_data列表中
    all_data.append(json_object)

# 打印所有的数据
for data in all_data:
    print(data)


# 将字符串转换为字典
all_data_parsed = [json.loads(item) for item in all_data]

# 提取numClients列表
numClients = [item['numClients'] for item in all_data_parsed]

# 定义操作和参数列表
operations = ['write', 'read']
parameters = ['Total Transferred', 'Total Throughput', 'Total Duration',
              'times Max', 'times 99th %ile', 'times Min']

# 使用嵌套的列表推导式来提取数据
data = {operation: {parameter: [item[operation][parameter.replace('times', operation.capitalize() + ' times')] for item in all_data_parsed]
                    for parameter in parameters} for operation in operations}

# 遍历每个参数，对于每个参数，遍历每个操作
for parameter in parameters:
    plt.figure()
    for operation in operations:
        # 提取参数数据
        parameter_data = data[operation][parameter]

        # 在图表上绘制参数
        plt.plot(numClients, parameter_data,
                 label=f'{operation} {parameter}')

    plt.title(f'numClients vs {parameter}')
    plt.xlabel('numClients')
    plt.ylabel(parameter)
    plt.legend()
    plt.show()
