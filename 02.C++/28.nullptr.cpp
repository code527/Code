/*************************************************************************
	> File Name: 28.nullptr.cpp
	> Author: 
	> Mail: 
	> Created Time: 日 10/ 4 19:23:12 2020
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

void f(int x) {
    cout << x << endl;
    return ;
}

void f(int *p) {
    cout << p << endl;
    return ;
}

int main() {
    int n = 123;
    f(n);
    f(&n);
    f(nullptr);
    return 0;
}
