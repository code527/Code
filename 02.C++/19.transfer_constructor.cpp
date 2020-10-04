/*************************************************************************
	> File Name: 19.transfer_constructor.cpp
	> Author: 
	> Mail: 
	> Created Time: 日 10/ 4 11:44:06 2020
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

class BigInt {
public :
    BigInt() {}
    BigInt(int x) {
        num.push_back(x);
        proccess_digit();
    }
    
    friend ostream &operator<<(ostream &, const BigInt &);
private:
    vector<int> num;
    void proccess_digit() {
        for (int i = 0; i < num.size(); i++) {
            if (num[i] < 10) continue;
            if (i + 1== num.size()) num.push_back(0);
            num[i + 1] = num[i] / 10;
            num[i] %= 10;
        }
        return ;
    }
};

ostream &operator<<(ostream &out, const BigInt &a) {
    for (int i = a.num.size() - 1; i >= 0; i--) {
        out << a.num[i];
    }
    return out;
}

void func(BigInt a) {
    cout << "func : " << a << endl;
}

int main() {
    BigInt a;
    a = 1234;
    cout << a << endl;
    func(5670);
    return 0;
}
