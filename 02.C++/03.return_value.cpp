/*************************************************************************
	> File Name: 03.return_value.cpp
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 日  6/23 18:58:17 2019
 ************************************************************************/

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <vector>
#include <map>
#include <cmath>
using namespace std;

class A {
public :
    A() {
        cout << this << " constructor" << endl;
    }
    A(const A &obj) {
        cout << this << " copy constructor" << endl;
    }
    A &operator=(const A &obj) {
        cout << this << " operator = "<< endl;
        return *this;
    }
    ~A() {
        cout << this << " destructor" << endl;
    }
};

A func() {
    A temp;
    cout << &temp << endl;
    return temp;
}

int main() {
    A a = func();
    cout << &a << endl;
    return 0;
}
