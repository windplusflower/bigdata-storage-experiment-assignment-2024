# 实验名称
    搭建对象存储
# 实验环境
    Ubuntu 22.04
# 实验记录
## Docker环境配置
    1. 安装docker依赖 : apt-get install ca-certificates curl gnupg lsb-release apt-transport-https software-properties-common
    2. 添加Docker官方GPG密钥 : curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
    3. 添加Docker软件源 : sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
    4. 安装docker : apt-get install docker-ce docker-ce-cli containerd.io
    5. 配置用户组 : sudo usermod -aG docker $USER
    6. 重启docker : service docker restart
    7. 验证是否成功: sudo docker run hello-world
## Swift运行记录
    编写swift.sh来复用命令
* swift.sh run : 启动openstack-swift
* swift.sh stop : 停止openstack-swift
* swift.sh test_stat : 测试 stat
* swift.sh test_list : 测试 list
* swift.sh test_connect : 测试命令行上传下载功能
* swift.sh test_all : 执行所有测试
# 实验小结
    按照官方文档逐步实现即可