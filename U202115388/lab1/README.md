# 搭建对象存储

# 实验环境
## 设备规格
* 设备名称	LAPTOP-H9DSJ8FK
* 处理器	AMD Ryzen 7 5800H with Radeon Graphics            3.20 GHz
* 机带 RAM	16.0 GB (15.9 GB 可用)
* 设备 ID	F26C7E32-5B2E-4EA7-802C-D25677D53F27
* 产品 ID	00342-36189-43009-AAOEM
* 系统类型	64 位操作系统, 基于 x64 的处理器
* 笔和触控	没有可用于此显示器的笔或触控输入

## Windows规格
* 版本	Windows 10 家庭中文版
* 版本号	22H2
* 安装日期	‎2021/‎6/‎22
* 操作系统内部版本	19045.4170
* 序列号	PF2TSPDV
* 体验	Windows Feature Experience Pack 1000.19054.1000.0


# 实验记录

## 实验lab1-1：安装Openstack swift镜像
从[dockerhub](https://hub.docker.com/r/dockerswiftaio/docker-swift)中找到openstack-swift的镜像，然后拉取即可

![拉取dockerswiftaio/docker-swift](./figure/image-3.png)
<!-- ![拉取镜像并进入](image.png) -->
## 实验lab1-2：启动
使用docker run让一个镜像```dockerswiftaio/docker-swift```启动一个容器openstack-swift

![启动](./figure/image-4.png)

<!-- ![启动ceph](image-1.png) -->
查看容器的日志，如下。说明存储系统服务器端已搭建完成

![日志](./figure/image-5.png)

# 实验小结
* 在这个实验中，我选用了openstack swift，搭建了存储系统服务器端。
