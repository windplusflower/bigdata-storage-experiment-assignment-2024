# 实验名称

LAB 1 - 搭建对象存储

# 实验环境

| | |
| :----- | :----- | 
| 操作系统 | Microsoft Window 10 Home Single Language |
| 处理器 | Intel(R) Core(TM) i7-10750H CPU @ 2.60Ghz |
| 软件 | minIO server |

# 实验记录-LAB1

**第一步：环境安装与设置**

在官网中`min.io`下载minIO Server和mc


**第二步：运行**

在存放minio.exe的文件夹中打开cmd并运行下列指令：

`minio.exe server filepath`

其中，使用真实存放minio.exe的文件路径替换代码中的filepath；


**第三步：执行**

在第二步的运行结果中找到*WebUI*行，其提供了网址，登入用户名及密码

![LAB1_1](/Users/pings/Desktop/BigData/bigdata-storage-experiment-assignment-2024/I202120037/Lab1/figure/LAB1_1.JPG)

选择其中一个网址，并复制到浏览器中打开

![LAB1_2](/Users/pings/Desktop/BigData/bigdata-storage-experiment-assignment-2024/I202120037/Lab1/figure/LAB1_2.JPG)

输入用户名及密码进入，成功进入即访问正常。

![LAB1_3](/Users/pings/Desktop/BigData/bigdata-storage-experiment-assignment-2024/I202120037/Lab1/figure/LAB1_3.JPG)

创建一个新桶（mytest）用于后续测试

![LAB1_4](/Users/pings/Desktop/BigData/bigdata-storage-experiment-assignment-2024/I202120037/Lab1/figure/LAB1_4.JPG)

# 实验小结

初步了解了对象存储技术，实现了对象存储的服务器端。