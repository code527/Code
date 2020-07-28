/*************************************************************************
	> File Name: 10.hash_table.cpp
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 四  7/18 12:23:46 2019
 ************************************************************************/

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <vector>
#include <map>
#include <unordered_map>
#include <cmath>
#include "10.hash_table.h"
using namespace std;

struct A {
    A(int x, int y) : x(x), y(y) {}
    int x, y;
    bool operator==(A const &a) const {
        return this->x == a.x && this->y == a.y;
    }
};

struct myhash {
    int operator()(A const &a) const {
        return a.x + a.y;
    }
};

int main() {
    A a(0, 9), b(10, 12);
    unordered_map<A, int, myhash> arr;
    arr[a] = 1;
    arr[b] = 2;
    cout << arr[a] << endl;
    cout << arr[b] << endl;
    haizei::unordered_map<int, int> arr2;
    arr2[129883] = 65;
    arr2[623] = 23;
    cout << arr2[129883] << endl;
    cout << arr2[623] << endl;

    haizei::unordered_map<A, int, myhash> arr3;
    arr3[a] = 1;
    arr3[b] = 2;
    cout << arr3[a] << endl;
    cout << arr3[b] << endl;
    return 0;
}
