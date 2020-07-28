/*************************************************************************
	> File Name: 14.single.cpp
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 日  3/29 17:36:12 2020
 ************************************************************************/

#include <iostream>
#include <algorithm>
using namespace std;

using namespace std;

struct SingleClass {
public :
    static SingleClass *getInstance() {
        static SingleClass *obj = nullptr;
        if (obj) return obj;
        obj = new SingleClass();
        return obj;
    }
private:
    SingleClass() {}
    SingleClass(const SingleClass &) {}
};

int main() {
    SingleClass *a = SingleClass::getInstance();
    return 0;
}
