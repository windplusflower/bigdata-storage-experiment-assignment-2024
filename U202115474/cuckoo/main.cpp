#include <iostream>
#include "lib/cuckoo.h"

const int elenum = 100;
void err(std::string s) {
    std::cout << s << std::endl;
    exit(-1);
}
void print(CuckooMap<int, int> f) {
    printf("******************map*****************\n");
    for (auto v : f) std::cout << v.first << ' ' << v.second << "\n";
    printf("******************end*****************\n");
}
void test() {
    //对f和tasks进行相同操作，它们内部的元素应该始终相同，以此来验证程序的正确性
    CuckooMap<int, int> f;
    std::unordered_map<int, int> tasks;

    auto check = [&]() {
        if (f.size() != tasks.size()) {
            printf("f.size is %d but tasks.size is %d\n", f.size(),
                   tasks.size());
            return 0;
        }
        for (auto v : f)
            if (tasks[v.first] != v.second) {
                printf("tasks has (%d,%d) but f has (%d,%d)\n", v.first,
                       tasks[v.first], v.first, v.second);
                return 0;
            }
        return 1;
    };
    srand(0);

    //测试insert
    for (int i = 1; i <= elenum; i++) {
        int a = rand(), b = rand();
        tasks.insert({a, b});
        f.insert(a, b);
        if (!check()) err("insert error");
    }

    //测试find
    for (int i = 0; i < elenum / 2; i++) {
        // tasks中随机选一个元素，在f中查找
        int pos = rand() % tasks.size();
        auto it = tasks.begin();
        while (pos--) it++;
        auto itr = f.find(it->first);
        if (it->second != itr->second) { err("find error!"); }
    }
    // find找不到的情况
    int temp = 0;
    while (tasks.count(temp)) temp++;
    if (f.find(temp) != f.end()) err("find er error!");

    //测试count
    for (int i = 0; i < elenum; i++) {
        int temp = rand();
        if (f.count(temp) != tasks.count(temp)) err("count error!");
    }

    //测试erase
    for (int i = 0; i < elenum / 10; i++) {
        int pos = rand() % tasks.size();
        auto it = tasks.begin();
        while (pos--) it++;
        f.erase(it->first);
        tasks.erase(it);
        if (!check()) err("erase error!");
    }

    std::cout << "tests passed!" << std::endl;
}
int main() {
    test();
}
