//#pragma once
#include "hash.h"
#include <bits/stdc++.h>
#include <functional>

//用于扩容的size备选值，数值来源于STL
static const int size_num = 28;
static const unsigned long sizes[size_num] = {
    53,        97,          193,          389,         769,       1543,
    3079,      6151,        12289,        24593,       49157,     98317,
    196613,    393241,      786433,       1572869,     3145739,   6291469,
    12582917,  25165843,    50331653,     100663319,   201326611, 402653189,
    805306457, 16106122741, 3221225473ul, 4294967291ul};

// T是key的类型，P是value的类型
template <class T, class P>
class CuckooMap {
    //当前大小在sizes里的对应下标
    int size_pos;
    //当前大小
    int _size;
    //当前元素数量
    int num;
    //拥挤阈值
    double num_limits;
    //每个链表元素上限
    int num_per_bucket;
    // a和b两个链表数组
    std::vector<std::list<std::pair<T, P>>> a, b;
    //两个基准哈希函数,用于生成实际调用的哈希函数
    std::function<int(T)> Hash;
    //两个面具，用于rehash
    int maska, maskb;
    //冲突次数，指两桶均满的冲突
    int conflicts;
    // rehash次数，如果多了说明当前容量不行
    int rehashs;
    //开启调试模式
    bool debug;

public:
    //迭代器
    class iterator {
    public:
        typedef typename std::list<std::pair<T, P>>::iterator Iter;
        //链表指针
        Iter ptr;
        //父实例
        CuckooMap<T, P> &outer;
        //当前在哪个数组
        int vec_num;
        //在当前数组的第几个链表
        int pos;

    public:
        // 迭代器构造函数
        iterator(CuckooMap<T, P> &_outer, Iter p, int _vec_num, int _pos) :
            outer(_outer), ptr(p), vec_num(_vec_num), pos(_pos) {
        }
        // 指针解引用操作符重载
        std::pair<T, P> &operator*() {
            return *ptr;
        }
        //成员访问重载
        Iter operator->() {
            return ptr;
        }
        // 前缀自增操作符重载
        iterator &operator++() {
            ptr++;
            if (vec_num == 0) { //当前在a数组
                auto &vec = outer.a;
                if (ptr != vec[pos].end()) return *this;
                pos++;
                while (pos < vec.size()) {
                    if (!vec[pos].empty()) break;
                    pos++;
                }
                if (pos == vec.size()) {
                    vec_num = 1;
                    auto &Vec = outer.b;
                    pos = 0;
                    while (pos < Vec.size()) {
                        if (!Vec[pos].empty()) break;
                        pos++;
                    }
                    // b数组走到了最后，返回end
                    if (pos == Vec.size()) {
                        ptr = Vec.back().end();
                        return *this;
                    }
                    //在b数组中找到了
                    ptr = Vec[pos].begin();
                    return *this;
                }
                //在a数组找到了
                ptr = vec[pos].begin();
                return *this;
            } else { //当前在b数组
                auto &vec = outer.b;
                if (ptr != vec[pos].end()) return *this;
                pos++;
                while (pos < vec.size()) {
                    if (!vec[pos].empty()) break;
                    pos++;
                }
                // b数组走到了最后，返回end
                if (pos == vec.size()) {
                    ptr = vec.back().end();
                    return *this;
                }
                //在b数组中找到了
                ptr = vec[pos].begin();
                return *this;
            }
            //理论上不会走到这
            return *this;
        }

        // 后缀自增操作符重载
        iterator operator++(int) {
            // todo
            iterator temp = *this;
            ++*this;
            return temp;
        }
        // 比较操作符重载
        bool operator!=(const iterator &other) const {
            return ptr != other.ptr;
        };
        // 比较操作符重载
        bool operator==(const iterator &other) const {
            return ptr == other.ptr;
        };
    };
    //默认构造
    CuckooMap<T, P>() :
        size_pos(0), _size(sizes[0]), num(0), num_limits(0.1),
        num_per_bucket(16), debug(false), conflicts(0), maska(0), maskb(0),
        rehashs(0) {
        Hash_Generator<T> *hash_generator = new Hash_Generator<T>();
        Hash = hash_generator->alloc();
        a.resize(_size);
        b.resize(_size);
        delete hash_generator;
    }
    //指定哈希函数进行构造
    CuckooMap<T, P>(std::function<int(T)> _hash) :
        size_pos(0), _size(sizes[0]), Hash(_hash), num(0), num_limits(0.1),
        num_per_bucket(16), debug(false), conflicts(0), maska(0), maskb(0),
        rehashs(0) {
        a.resize(_size);
        b.resize(_size);
    }
    //析构函数
    ~CuckooMap<T, P>(){};

    //实际调用的哈希函数a
    int hasha(T key) {
        return Hash(key) ^ maska;
    }

    //实际调用的哈希函数b
    int hashb(T key) {
        return Hash(key) ^ maskb;
    }
    //清空
    void clear() {
        a.clear();
        b.clear();
        num = 0;
    }
    //判断是否需要扩容
    bool need_enlarge() {
        return 1.0 * num / (_size * 2 * num_per_bucket) > num_limits;
    }

    //扩容
    void enlarge() {
        if (debug) printf("enter enlage\n");
        size_pos++;
        int oldsize = _size;
        _size = sizes[size_pos];
        /*  这是enlarge的老代码，新代码优化后速度提升了一倍
        std::vector<std::list<std::pair<T, P>>> temp;
        for (auto &v : a) temp.push_back(std::move(v));
        for (auto &v : b) temp.push_back(std::move(v));
        clear();
        a.resize(_size);
        b.resize(_size);
        for (auto list : temp)
            for (auto v : list) insert(v.first, v.second);
        */

        a.resize(_size);
        b.resize(_size);
        //同一个链表内的元素在扩容后不一定在同一个链表内，因此不能整个链表转移
        for (int i = 0; i < oldsize; i++) {
            if (a[i].empty()) continue;
            auto it = a[i].begin();
            while (it != a[i].end()) {
                int posa = hasha(it->first) % _size;
                if (posa == i) {
                    it++;
                    continue;
                }
                a[posa].push_back(*it);
                it = a[i].erase(it);
            }
        }
        for (int i = 0; i < oldsize; i++) {
            if (b[i].empty()) continue;
            auto it = b[i].begin();
            while (it != b[i].end()) {
                int posb = hashb(it->first) % _size;
                if (posb == i) {
                    it++;
                    continue;
                }
                b[posb].push_back(*it);
                it = b[i].erase(it);
            }
        }
        debug_info();
    }
    //修改阈值
    void change_limits(double _limits) {
        num_limits = _limits;
        if (need_enlarge()) enlarge();
    }

    //修改每个链表的元素上限
    void change_num_limits(int _nums) {
        num_per_bucket = _nums;
        shrink();
    }
    //插入键值对
    void insert(const T &key, const P &value) {
        if (need_rehash()) rehash();
        iterator it = find(key);
        if (it != end()) { //原本就在
            it->second = value;
            return;
        }
        //新增键值对
        if (need_enlarge()) enlarge();
        num++;
        int posa = hasha(key) % _size;
        int posb = hashb(key) % _size;
        if (debug) printf("insert key %d to pos(%d,%d)\n", key, posa, posb);
        //没满就加到较小的桶里
        if (a[posa].size() > b[posb].size()) {
            b[posb].emplace_back(key, value);
            //类似拥塞控制的指数下降，线性增长
            conflicts /= 2;
        } else if (a[posa].size() < num_per_bucket) {
            a[posa].emplace_back(key, value);
            conflicts /= 2;
        } else {
            //虽然弹出的元素如果也全满，直接调用插入有二分之一的概率选到同一个桶，但由于添加元素是从桶位加，
            //弹出元素是从桶头弹，因此选中的不是同一个元素，与另选一个桶没有区别。
            num--;
            conflicts++;
            if (time(0) % 2) {
                auto temp = a[posa].front();
                a[posa].pop_front();
                a[posa].emplace_back(key, value);
                insert(temp.first, temp.second);
            } else {
                auto temp = a[posb].front();
                a[posa].pop_front();
                a[posa].emplace_back(key, value);
                insert(temp.first, temp.second);
            }
        }
    }

    //插入pair
    void insert(std::pair<T, P> p) {
        insert(p.first, p.second);
    }

    //重载[]
    P &operator[](T key) {
        if (count(key)) return find(key)->second;
        P temp;
        bzero(&temp, sizeof(temp));
        insert(key, temp);
        return find(key)->second;
    }

    //删除键值对,返回下一个元素的迭代器
    iterator erase(iterator it) {
        iterator nxt = it;
        nxt++;
        if (it.vec_num == 0) {
            it.outer.a[it.pos].erase(it.ptr);
        } else {
            it.outer.b[it.pos].erase(it.ptr);
        }
        num--;
        return nxt;
    }
    //删除键值对,返回下一个元素的迭代器
    iterator erase(const T &key) {
        iterator it = find(key);
        return erase(it);
    }
    //查找键值对
    iterator find(const T &key) {
        int posa = hasha(key) % _size;
        int posb = hashb(key) % _size;
        if (debug) {
            printf("(%d,%d)\n", posa, a.size());
            std::cout << std::endl;
        }
        for (auto it = a[posa].begin(); it != a[posa].end(); it++)
            if (it->first == key) return iterator(*this, it, 0, posa);
        for (auto it = b[posb].begin(); it != b[posb].end(); it++)
            if (it->first == key) return iterator(*this, it, 1, posa);
        return end();
    }
    //键值对计数(其实只有0或1)
    int count(const T &key) {
        return find(key) != end();
    }
    //首
    iterator begin() {
        for (int i = 0; i < a.size(); i++)
            if (!a[i].empty()) return iterator(*this, a[i].begin(), 0, i);
        for (int i = 0; i < b.size(); i++)
            if (!b[i].empty()) return iterator(*this, b[i].begin(), 0, i);
        return end();
    }

    //尾
    iterator end() {
        return iterator(*this, b.back().end(), 1, b.size() - 1);
    }

    //返回键值对数量
    int size() {
        return num;
    }

    //输出哈希表信息
    void debug_info() {
        if (!debug) return;
        printf("\n*********vec a***********\n");
        for (int i = 0; i < _size; i++) {
            printf("list %d : ", i);
            for (auto v : a[i]) printf("(%d,%d) ", v.first, v.second);
            printf("\n");
        }
        printf("*********vec b***********\n");
        for (int i = 0; i < _size; i++) {
            printf("list %d : ", i);
            for (auto v : b[i]) printf("(%d,%d) ", v.first, v.second);
            printf("\n");
        }
        printf("***********end************\n\n");
    }

    //开启调试模式
    void debug_on() {
        debug = true;
    }

    //需要重新哈希
    bool need_rehash() {
        return conflicts > num_per_bucket * 2;
    }
    //重新哈希
    //因为可能是用户自定义的哈希函数，所以不能调用Hash_Generator
    void rehash() {
        conflicts = 0;
        if (debug) printf("enter rehash\n");
        // rehashs后依旧失败，选择扩容
        if (rehashs && size_pos != 27) {
            enlarge();
            return;
        }
        rehashs++;
        //容量已经是最大，再考虑重新哈希
        maska = std::hash<int>()(time(0));
        maskb = std::hash<int>()(time(0));
        //重新哈希的操作其实跟扩容一样，只是不需要扩容，因此代码可以复用
        size_pos--;
        enlarge();
        //重新hash后可能有些链表元素数量不满足num_per_list
        shrink();
        //能跑到这里说明shrink运行成功了，新的哈希表成功保存了所有函数
        //否则shink运行过程中会再次递归触发rehash
        rehashs = 0;
    }

    //调整过长的链表，只在修改nums_per_list和rehash后使用
    void shrink() {
        std::vector<std::pair<T, P>> temp;
        for (auto &v : a)
            while (v.size() > num_per_bucket) {
                temp.push_back(v.back());
                v.pop_back();
            }
        for (auto &v : b)
            while (v.size() > num_per_bucket) {
                temp.push_back(v.back());
                v.pop_back();
            }
        for (auto v : temp) insert(v);
    }

    //是否为空
    bool empty() {
        return num == 0;
    }
};