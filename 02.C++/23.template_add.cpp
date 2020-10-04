/*************************************************************************
	> File Name: 23.template_add.cpp
	> Author: 
	> Mail: 
	> Created Time: 日 10/ 4 18:36:11 2020
 ************************************************************************/

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <vector>
#include <map>
#include <cmath>
#include <queue>
using namespace std;

struct A {
    A() = delete;
    A(int x) : x(x) {}
    double operator+(int x) {
        return x + this->x + 0.001;
    }
    int x;
};

template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

template<typename T, typename U>
auto add(T *a, U *b) -> decltype(add(*a, *b)) {
    return add(*a, *b);
}

auto func(int x) -> int {
    return 2 * x;
}

int main() {
    cout << add(2, 3) << endl;
    cout << add(2.3, 3.5) << endl;
    cout << add(2, 3.5) << endl;
    cout << add(3.5, 2) << endl;
    int a = 12;
    double b = 45.7;
    decltype(a + b) c;
    cout << sizeof(c) << endl;
    A d(6);
    cout << add(d, 4) << endl;
    cout << func(4) << endl;
    cout << add(a, b) << endl;
    cout << add(&a, &b) << endl;
    return 0;
}
