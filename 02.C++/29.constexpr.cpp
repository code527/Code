/*************************************************************************
	> File Name: 29.constexpr.cpp
	> Author: 
	> Mail: 
	> Created Time: 日 10/ 4 19:29:54 2020
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

constexpr int f(int i) {
    return 2 * i;
}

struct A {
    constexpr A(int x, int y) : x(x), y(y) {}
    int x, y;
};

int main() {
    int n;
    cin >> n;
    const int a = n + 3;
    constexpr int b = f(123) + 567;
    cout << f(n) << endl;
    constexpr A c(2, 3);
    A d(n, 4);
    return 0;
}
