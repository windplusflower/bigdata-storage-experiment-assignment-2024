#pragma once
#include <bits/stdc++.h>
template <class T>
class Hash_Generator {
public:
    std::function<int(T)> alloc() {
        int mask = std::hash<int>()(time(0));
        return [=](T a) { return std::hash<T>()(a) ^ mask; };
    };
};