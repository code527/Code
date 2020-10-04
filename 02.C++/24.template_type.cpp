/*************************************************************************
	> File Name: 24.template_type.cpp
	> Author: 
	> Mail: 
	> Created Time: 日 10/ 4 18:37:33 2020
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
#include <functional>
using namespace std;

template<typename T>
void my_swap(T &&a, T &&b) {
    typename remove_reference<T>::type c;
    c = a;
    a = b;
    b = c;
    return ;
}

template<typename T>
void add(T &&a, T &&b) {
    a += 3;
    b += 4;
    return ;
}

void func(void (*p)(int &, int &), int &a, int &b) {
    p(a, b);
    return ;
}

template<typename T>
typename remove_reference<T>::type &&my_move(T &&a) {
    return static_cast<typename remove_reference<T>::type &&>(a);
}

template<typename T>
struct my_remove_reference {
    typedef T type;
};

template<typename T>
struct my_remove_reference<T &> {
    typedef T type;
};

template<typename T>
struct my_remove_reference<T &&> {
    typedef T type;
};

void func(int &a) {
    cout << "left value" << endl;
}

void func(int &&a) {
    cout << "right value" << endl;
}

int main() {
    int a = 123, b = 456;
    cout << a << " " << b << endl;
    my_swap(a, b);
    cout << a << " " << b << endl;
    my_swap(move(a), move(b));
    cout << a << " " << b << endl;
    func(add, a, b);
    cout << a << " " << b << endl;
    my_swap(my_move(a), my_move(b));
    func(a);
    func(my_move(a));
    typename my_remove_reference<int>::type c;
    typename my_remove_reference<int &>::type d;
    typename my_remove_reference<int &&>::type e;
    return 0;
}
