/*************************************************************************
	> File Name: 08.hashtable.cpp
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 四  7/11 15:30:11 2019
 ************************************************************************/

#include <iostream>
#include <algorithm>
#include "08.hashtable.h"
using namespace std;

class MyHash1 : public HashFunc {
public :
    int operator()(const void *value) {
        const char *str = (const char *)(value);
        int hash_code = 0, seed = 131;
        while (*str) {
            hash_code = hash_code * seed + str[0];
            str++;
        }
        return hash_code & 0x7fffffff;
    }
};

int MyHash2(const void *data) {
    const char *str = (const char *)(data);
    int hash_code = 0, i = 0;
    while (*str) {
        if (i & 1) {
            hash_code ^= (hash_code << 7) ^ str[0] ^ (hash_code >> 3);
        } else {
            hash_code ^= (~((hash_code << 11) ^ str[0] ^ (hash_code >> 5)));
        }
        ++str, ++i;
    }
    return hash_code & 0x7fffffff;
}

int main() {
    MyHash1 func1;
    HashTable h1(func1), h2(MyHash2);
    cout << h1.get_hash("hello world") << endl;
    cout << h1.get_hash("hello haizei") << endl;
    cout << h2.get_hash("hello world") << endl;
    cout << h2.get_hash("hello haizei") << endl;
    return 0;
}
