# 实验名称

搭建对象存储

## 实验环境

```shell
       /\         rick@ricksarchlinux
      /  \        os     Arch Linux
     /\   \       host   82JW Lenovo Legion R7000P2021
    /      \      kernel 6.8.1-arch1-1
   /   ,,   \     uptime 3h 20m
  /   |  |  -\    pkgs   1368
 /_-''    ''-_\   memory 6250M / 13830M
```

## 实验操作

本地搭建 minio 服务

创建对应的数据文件夹后

```shell
docker run \
--name minio \
-p 9000:9000  \
-p 9090:9090  \
-d \
-e "MINIO_ROOT_USER=minio" \
-e "MINIO_ROOT_PASSWORD=minio123" \
-v /home/rick/minio-data:/data \
-v /home/rick/minio-config:/root/.minio \
minio/minio server  /data --console-address ":9090" --address ":9000"
```
