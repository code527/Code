/*************************************************************************
	> File Name: 34.prime_thread.cpp
	> Author: 
	> Mail: 
	> Created Time: 一 10/ 5 16:32:59 2020
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
#include "35.thread_pool.h"
using namespace std;

int is_prime(int x) {
    if (x <= 1) return 0;
    for (int i = 2; i * i <= x; i++) {
        if (x % i == 0) return 0;
    }
    return 1;
}

void prime_cnt(int &ans, int l, int r) {
    int cnt = 0;
    for (int i = l; i <= r; i++) {
        cnt += is_prime(i);
    }
    __sync_fetch_and_add(&ans, cnt);
    return ;
}

int main() {
    int cnt = 0;
    haizei::thread_pool tp(5);
    tp.start();
    for (int i = 1; i <= 10; i++) {
        tp.add_one_task(prime_cnt, ref(cnt), (i - 1) * 100000 + 1, i * 100000);
    }
    tp.stop_until_empty();
    cout << cnt << endl;
    return 0;
}
