# 实验名称

# 实验环境
Unbantu 22.04
# 试验记录
## 实验1 运行s3-bench-rs
ppt中给出的s3-bench-rs是三年前的库了，其中有个crate rust-s3更新了很多版，接口发生过更改，已无法正常使用，新的接口对部分参数引入了生命周期的限制，使用略复杂，暂时不太会修改。不过好在作者当时提交过pull request到rust-s3，所以可以使用`git reset 8e41`来回退到正确的版本。

服务端使用minio，运行结果如下：
![](figure/run_bench.png)
# 实验小结
......