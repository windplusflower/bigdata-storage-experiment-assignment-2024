# 实验名称

Lab 1 搭建对象存储

# 实验环境

处理器	11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz   2.69 GHz  
系统类型	64 位操作系统, 基于 x64 的处理器  
git version 2.41.0.windows.2  
服务器 s3proxy
客户端 aws-shell
# 实验记录
## 实验1-1：服务端

> 使用**S3Proxy**模拟AWS S3服务

1. 下载 S3Proxy release包
2. 配置config文件，config文件内容如下：
```java
s3proxy.authorization=none
s3proxy.endpoint=http://127.0.0.1:8080
jclouds.provider=filesystem
jclouds.filesystem.basedir=/tmp/s3proxy
```
3. 创建文件系统目录
```
mkdir /tmp/s3proxy
```
4. 运行S3proxy服务
```
java -jar s3proxy --properties s3proxy.conf
```
![](figure/Snipaste_2024-04-02_18-52-27.png)
5. 在浏览器中查看详情
![](figure/Snipaste_2024-04-02_18-57-05.png)
## 实验1-2：客户端

>使用aws-shell工具集

1.下载aws-shell
```
pip install s3cmd
```
2.配置.aws/config文件
```
[default]
region = cn-north-1
output = json
endpoint_url = http://127.0.0.1:8080
```
3.运行aws-shell
![](figure/Snipaste_2024-04-02_19-03-27.png)
# 实验小结

使用S3-Proxy+aws-shell搭建了对象存储系统