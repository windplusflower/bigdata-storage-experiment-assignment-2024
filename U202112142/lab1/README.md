# 实验名称

……

# 实验环境

……

# 实验记录

## 实验1-1：……
因为本地已有linux系统和python环境，该部分不赘述
首先尝试入门的minIO
下载docker
sudo apt-get docker-ce
然后获取MinIO的Docker镜像
docker pull minio/minio
运行docker 
docker run -p 9000:9000 \
  -e "MINIO_ACCESS_KEY=youraccesskey" \
  -e "MINIO_SECRET_KEY=yoursecretkey" \
  minio/minio server /data
在另一个终端运行lab1中的minIO.py文件
完成文件的上传与下载

# 实验小结

……