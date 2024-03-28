# 实验名称

Lab1 搭建对象存储

# 实验环境

Minio Server: （虚拟机环境）CentOS 7.9
Minio Client:  Windows 10

# 实验记录

## 实验1-1：使用docker搭建Minio Server
首先在虚拟机上安装docker：

``yum install docker-ce docker-ce-cli containerd.io``

检测docker安装成功：

`systemctl start docker`

`docker run hello-world`

用docker直接下载Minio最新版镜像：

`docker pull minio/minio`

配置并启动Minio Server：（首先建立/minio/config和data目录）
```bash
docker run -p 9000:9000 -p 9090:9090 \
>      --net=host \
>      --name minio \
>      -d --restart=always \
>      -e "MINIO_ACCESS_KEY=minioadmin" \
>      -e "MINIO_SECRET_KEY=minioadmin" \
>      -v /home/minio/data:/data \
>      -v /home/minio/config:/root/.minio \
>      minio/minio server \
>      /data --console-address ":9090" -address ":9000"

```

在浏览器访问Minio Server成功：

<img src=".\figure\1 minioserver.png">

创建一个新bucket：test-bucket

<img src=".\figure\2 test-bucket.png">

## 实验1-2：配置Minio Client
从Minio官网下载mc.exe，配置Minio Client：

`.\mc config host add myminio http://192.168.194.101:9000 minioadmin minioadmin`

列出当前Server上的桶：

`.\mc ls myminio`

<img src=".\figure\3 minioclient.png">