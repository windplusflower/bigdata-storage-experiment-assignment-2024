在此目录运行 `make build` 可以在此目录生成测试程序的可执行文件cuckoo

在此目录运行 `make run` 可以自动运行cuckoo的测试程序

lib内实现了`CuckooMap`类，它实现了`insert`、`find`、`erase`等多个成员函数，实现了迭代器、动态扩容等功能，并且提供了接口调节默认的填充因子、桶的容量等信息，使用方式基本与std::unordered_map相同，详见lib/cuckoo.h