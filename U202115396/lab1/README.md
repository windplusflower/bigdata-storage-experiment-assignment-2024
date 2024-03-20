# 实验名称

搭建对象存储

# 实验环境


| 操作系统 | Windows 11 专业版                                          |
| ---------- | ------------------------------------------------------------ |
| 处理器   | AMD Ryzen 5 4600U with Radeon Graphics            2.10 GHz |
| 内存     | 16G                                                        |
| 服务器端 | MinIO Server                                               |
| 系统类型 | 64 位操作系统, 基于 x64 的处理器                           |

# 实验记录

## 实验lab1

1. 直接在Minio官网下载Minio Server的windows版本

   ![1710894014706.png](./figure/1710894014706.png)
2. 进入minio.exe存放路径，打开cmd, 输入命令 `minio.exe  server path`,path是minio.exe所在的文件路径

   ![1710894174756.png](./figure/1710894174756.png)
3. 复制一个WebUI，在浏览器中打开，然后输入用户名和密码，`minioadmin`,进入Minio Server界面。![1710894311335.png](./figure/1710894311335.png)
4. 界面如下：（Minio Server会把与minio.exe同目录下的文件夹初始化为空桶）

   ![1710894390081.png](./figure/1710894390081.png)

# 实验小结
