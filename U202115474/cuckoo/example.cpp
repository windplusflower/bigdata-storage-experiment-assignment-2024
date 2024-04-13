#include "lib/cuckoo.h"
struct P {
    int x;
    int y;
    bool operator==(P a) {
        return x == a.x && y == a.y;
    }
};
int main() {
    //创建map
    CuckooMap<int, int> f;
    //自定义的类型也能使用，需要手动传哈希函数
    CuckooMap<P, std::string> fp(
        [](P a) { return std::hash<int>()(a.x) ^ std::hash<int>()(a.y); });
    // insert可以插入键值对，也可以直接插入pair，还可以用[]，也能用迭代器
    fp.insert({1, 2}, "hello world");
    fp.insert({{7, 9}, "hello cuckoo"});
    fp[{3, 4}] = "hello kitty";
    auto itfp = fp.begin();
    itfp->second += " 666";
    for (int i = 0; i < 10; i++) f.insert({rand(), rand()});
    //可以使用:语法遍历
    for (auto v : fp) {
        printf("{(%d,%d),%s}\n", v.first.x, v.first.y, v.second.c_str());
    }
    //也可以用迭代器
    for (auto it = f.begin(); it != f.end(); it++)
        printf("(%d,%d) \n", it->first, it->second);
    //调整动态扩容的阈值（元素数量除以最大容量），默认是0.1
    f.change_limits(0.5);
    //调整每个地址可开放寻址的元素数量,默认是16
    f.change_num_limits(2);
    //清空
    f.clear();
    //判断是否为空
    printf("f.empty=%d fp.empty=%d\n", f.empty(), fp.empty());
    //查找
    assert(fp.find({1, 3}) == fp.end());
    auto it = fp.find({7, 9});
    printf("{(%d,%d),%s}\n", it->first.x, it->first.y, it->second.c_str());
    printf("count {1,2}=%d  count {2,5}=%d\n", fp.count({1, 2}),
           fp.count({1, 5}));
    //删除
    fp.erase(it);
    //查看元素数量
    printf("size of fp is %d now\n", fp.size());
}