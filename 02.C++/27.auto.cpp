/*************************************************************************
	> File Name: 27.auto.cpp
	> Author: 
	> Mail: 
	> Created Time: 日 10/ 4 19:22:00 2020
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

string randstring(int n) {
    string ret = "";
    for (int i =0; i < n; i++) {
        char ch = rand() % 26 + 'A';
        ret += ch;
    }
    return ret;
}

int my_seed = 1;
void my_srand(int seed) {
    my_seed = seed;
}

int my_rand() {
    my_seed = my_seed * 3 % 101;
    return my_seed;
}

int main() {
    my_srand(time(0));
    for (int i = 0; i < 100; i++) {
        cout << my_rand() << endl;
    }
    srand(time(0));
    map<string, int> ind;
    for (int i = 0; i < 10; i++) {
        ind[randstring(rand() % 10 + 3)] = rand();
    }
    auto iter = ind.begin();
    for (; iter != ind.end(); iter++) {
        cout << iter->first << " " << iter->second << endl;
    }
    for (auto x : ind) {
        cout << x.first << " " << x.second << endl;
    }
    return 0;
}
