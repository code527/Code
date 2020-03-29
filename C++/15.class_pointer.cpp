/*************************************************************************
	> File Name: 15.class_pointer.cpp
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 日  3/29 17:37:57 2020
 ************************************************************************/

#include <iostream>
#include <algorithm>
using namespace std;

class A {
public :
    void say1() {
        cout << "say 1" << endl;
    }
    void say2() {
        cout << "say 2" << endl;
    }
    void say3() {
        cout << "say 3" << endl;
    }
};

void (A::*func[3])() = {&A::say1, &A::say2, &A::say3};

int main() {
    srand(time(0));
    A a, *p = &a;
    for (int i = 0; i < 20; i++) {
        (a.*func[rand() % 3])();
    }
    return 0;
}
