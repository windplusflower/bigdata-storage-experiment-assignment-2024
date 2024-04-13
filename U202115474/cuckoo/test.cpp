#include <ctime>
#include <iostream>
#include "lib/cuckoo.h"

const int test_num = 100;
const int speed_num = 1000000;
void err(std::string s) {
    std::cout << s << std::endl;
    exit(-1);
}
void print(CuckooMap<int, int> f) {
    printf("******************map*****************\n");
    for (auto v : f) std::cout << v.first << ' ' << v.second << "\n";
    printf("******************end*****************\n");
}
void debug() {
    CuckooMap<int, int> f;
    f.change_limits(0.8);
    f.change_num_limits(1);
    f.debug_on();
    for (int i = 0; i < 8; i++) {
        f.insert(rand(), 1);
        f.debug_info();
    }
}
void test() {
    //对f和tasks进行相同操作，它们内部的元素应该始终相同，以此来验证程序的正确性
    CuckooMap<int, int> f;
    std::unordered_map<int, int> tasks;

    auto check = [&]() {
        if (f.size() != tasks.size()) {
            printf("f.size is %d but tasks.size is %zu\n", f.size(),
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
    srand(time(0));

    //测试insert
    std::cout << "start testing insert\n";
    for (int i = 1; i <= test_num; i++) {
        int a = rand(), b = rand();
        tasks.insert({a, b});
        f.insert(a, b);
        if (!check()) err("insert error");
        f.debug_info();
    }

    //测试find
    printf("start testing find\n");
    for (int i = 0; i < test_num / 2; i++) {
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
    printf("start testing count\n");
    for (int i = 0; i < test_num; i++) {
        int temp = rand();
        if (f.count(temp) != tasks.count(temp)) err("count error!");
    }

    //测试erase
    printf("start testing erase");
    for (int i = 0; i < test_num / 10; i++) {
        int pos = rand() % tasks.size();
        auto it = tasks.begin();
        while (pos--) it++;
        f.erase(it->first);
        tasks.erase(it);
        if (!check()) err("erase error!");
    }

    std::cout << "\nAll tests passed!" << std::endl;
}
void speed() {
    std::vector<std::pair<int, int>> tasks;
    srand(time(0));
    for (int i = 0; i < speed_num; i++) { tasks.emplace_back(rand(), rand()); }
    std::vector<int> nums = {4, 8, 16, 32, 64, 128};
    for (auto v : nums) {
        CuckooMap<int, int> f;
        f.change_num_limits(v);
        clock_t bg = clock();
        for (auto a : tasks) f.insert(a);
        clock_t ed = clock();
        printf("insert %d elements spent %.2lf sec with bucket size %d.\n",
               speed_num, (ed - bg) / 1.0 / CLOCKS_PER_SEC, v);
    }
}
int main() {
    // debug();
    test();
    speed();
}
