# 实验名称

LAB 0 - 准备

# 实验环境

| | |
| :----- | :----- | 
| 操作系统 | Microsoft Window 10 Home Single Language |
| 处理器 | Intel(R) Core(TM) i7-10750H CPU @ 2.60Ghz |

# 实验记录-LAB0

**第一步：FORK**

使用FORK功能把总作业库复制到自己的作业库

**第二步：git clone**

在准备的路径中使用 git bash 运行 `git clone <repo URL>`，将作业库克隆到本地

需要注意的是，因为我是第一次使用git 所以需要到设置那里授权设置自己的 SSH Key

具体过程是 Settings -> SSH Keys and GPG Keys -> Create SSH Keys

**第三步：建立目录**

在克隆成功的本地作业库里建立I202120037目录

**第四步：完善目录**

在目录中分别创建 Lab 0 到 Lab 3 的文件夹作为子目录，每个子目录中各包含 Assert、figures和README文件

**第五步：git add**

完成 Lab 0 的内容后即可使用 `git add .\I202120037\` 将整个目录添加到git

**第六步：git commit**

`git commit -a -m ""` 提交所有未同步内容

**第七步：git push**

`git push` 将作业库更新到git仓库

**第八步：PULL Request**

向总库申请 PULL Request 将自己的作业合并到总库里


# 实验小结

学会使用git的基本功能。