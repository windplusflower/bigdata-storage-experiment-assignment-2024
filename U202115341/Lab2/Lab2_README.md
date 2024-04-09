# 实验名称

Lab2 实践基本功能

# 实验环境

Minio Server: （虚拟机环境）CentOS 7.9
Minio Client:  Windows 10

# 实验记录

## 实验2：执行CRUD操作
通过典型界面访问在 Lab 1 中搭建的系统，执行访问持久存储的4项基本操作。

在Windows端使用Minio Client完成。

Create 创建新bucket：

`.\mc mb myminio/mybucket`

<img src=".\figure\create.png">

Update 上传文件到bucket：

`.\mc cp test.txt myminio/mybucket`

<img src=".\figure\update.png">

Read 从服务端下载文件：

<img src=".\figure\download.png">

Delete 删除bucket中的文件，删除bucket：

`.\mc rm myminio/mybucket/test.txt`

`.\mc rb myminio/mybucket`

<img src=".\figure\delete.png">
