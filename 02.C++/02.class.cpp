/*************************************************************************
	> File Name: 02.class.cpp
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 日  6/23 16:00:20 2019
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

class Point {
public :
    Point() : _x(0), _y(0), _cnt(0) {
        this->total += 1;
        cout << "Point constructor : " << this << endl;
    }
    Point(int x, int y) : Point() {
        cout << "Point constructor with parameters : " << this << endl;
        this->_x = x;
        this->_y = y;
    }
    Point(const Point &b) : Point() {
        cout << "Point copy constructor : " << this << endl;
        this->_x = b._x;
        this->_y = b._y;
        this->_cnt = b._cnt;
    }
    int getX() const { 
        this->_cnt += 1;
        return this->_x;
    }
    int getY() const { return this->_y; }

    static int getTotal() { return Point::total; }
    
    ~Point() {
        this->total -= 1;
        cout << "Point destructor" << endl;
    }

private:
    int _x, _y;
    mutable int _cnt;

    static int total;
};

int Point::total = 0;

void func(Point &b) {
    cout << "b : " << (&b) << endl;
    return ;
}

ostream& operator<<(ostream &out, const Point &p) {
    out << "(" << p.getX() << ", " << p.getY() << ")";
    return out;
}

void func2() {
    Point a, b, c;
}

int main() {
    const Point p(4, 5);
    Point p1(p), p2(p1);
    func(p1);
    func2();
    cout << p1 << " " << p2 << endl;
    cout << Point::getTotal() << endl;
    return 0;
}
