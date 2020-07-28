/*************************************************************************
	> File Name: 07.virtual_table.cpp
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 四  7/11 15:26:36 2019
 ************************************************************************/

#include <iostream>
#include <algorithm>
using namespace std;

class A {
public :
    virtual void run(int x) {
        cout << "class A run" << endl;
    }
};
class B : public A {
public :
    void run(int x) {
        cout << "class B run" << endl;
        cout << this << endl;
        cout << x << endl;
    }
};

typedef void (*func)(void *, int);

int main() {
    B b;
    ((func **)(&b))[0][0](&b, 123);
    return 0;
}
