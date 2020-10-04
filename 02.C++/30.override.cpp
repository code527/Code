/*************************************************************************
	> File Name: 30.override.cpp
	> Author: 
	> Mail: 
	> Created Time: 日 10/ 4 19:30:56 2020
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

struct A {
    virtual void func1() final {
        cout << "Class A func yi" << endl;
    }
    void funcl() {
        cout << "Class A func ai ou" << endl;
    }
    virtual ~A() {
        cout << "A destructor" << endl;
    }
};

struct B : A {
    void func1() override {
        cout << "Class B func ai ou" << endl;
    }
    ~B() {
        cout << "B destructor" << endl;
    }
};

int main() {
    B b;
    A *a = &b, *c = new B();
    a->funcl();
    delete c;
    cout << "--------" << endl;
    return 0;
}
