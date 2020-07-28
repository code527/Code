/*************************************************************************
	> File Name: 11.left_right.cpp
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 日  3/29 16:47:49 2020
 ************************************************************************/

#include <iostream>
#include <algorithm>
using namespace std;
#define P(func, x) { \
    cout << #func << "(" << #x << ") "; \
    func(x); \
}


void Judge2(int &x) {
    cout << "left value" << endl;
    return ;
}

void Judge2(int &&x) {
    cout << "right value" << endl;
    return ;
}

void Judge(int &x) {
    cout << "left value" << endl;
    P(Judge2, forward<int &>(x));
    return ;
}

void Judge(int &&x) {
    cout << "right value" << endl;
    P(Judge2, forward<int &&>(x));
    return ;
}

int main() {
    int a = 1, b = 2;
    P(Judge, a);
    P(Judge, b);
    P(Judge, 123);
    P(Judge, a + b);
    P(Judge, a++);
    P(Judge, ++a);
    return 0;
}
