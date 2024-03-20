# 实验名称

实践基本功能

# 实验环境


| 操作系统 | Windows 11 专业版                                          |
| ---------- | ------------------------------------------------------------ |
| 处理器   | AMD Ryzen 5 4600U with Radeon Graphics            2.10 GHz |
| 内存     | 16G                                                        |
| 服务器端 | MinIO Server                                               |
| 系统类型 | 64 位操作系统, 基于 x64 的处理器                           |
| 客户端   | Boto3                                                      |

# 实验记录

## 实验lab2

1. 根据实验文档提供的Boto3源代码安装
   ```
   $ git clone https://github.com/boto/boto3.git
   $ cd boto3
   $ python -m pip install -r requirements.txt
   $ python -m pip install -e .
   ```
2. 建立Boto3客户端和Minio Server的连接
   1. 首先启动Minio Server
   2. 创建Minio Server的Access Keys,

      ![1710895880135.png](./figure/1710895880135.png)
   3. 修改test.py中的access_key,secret_key为自己创建好的密钥，同时修改endpoint_url为Minio Server正在运行的网址，然后就可以运行，从而测试客户端和服务端是否能够正确建立连接，如果能够正常建立连接，程序会打印出所有的存储桶。
3. Minio Server初始状态

![1710854045963.png](./figure/1710854045963.png)

4. 使用Create.py程序创建了一个新的存储桶`my-new-bucket`

![1710854343923.png](./figure/1710854343923.png)

5. `my-new-bucket`存储桶在更新前是一个空桶。

![1710854809531.png](./figure/1710854809531.png)

6. Update.py程序向`my-new-bucket`桶上传了一个文件`《深空彼岸》.txt`，其中object_key可以自行设置，但要保证不重复原则。

![1710854972524.png](./figure/1710854972524.png)

7. Read.py——读取：获取存储桶中的对象列表

![1710855063074.png](./figure/1710855063074.png)

8. Delete.py ——初始的时候，我又上传了一个新的文件，然后删除，这个时候再删除桶的时候发现报错——即如果桶不为空，则无法删除：

![1710855570490.png](./figure/1710855570490.png)

9. 更改删除代码——删除桶的所有文件，成功删除桶

![1710855655600.png](./figure/1710855655600.png)

# 实验小结
