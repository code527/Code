/************************************************************************
	> File Name: 13.visitor.cpp
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 日  3/29 17:34:27 2020
 ************************************************************************/

#include <iostream>
#include <algorithm>
using namespace std;

struct Cat;
struct Dog;
struct People;
struct Bat;

struct Animal {
    struct IVisitor {
        virtual void visit(Cat *) = 0;
        virtual void visit(Dog *) = 0;
        virtual void visit(People *) = 0;
        virtual void visit(Bat *) = 0;
    };
    virtual void say() = 0;
    virtual void Accept(IVisitor *) = 0;
};

struct Cat : Animal {
    void say() {
        cout << "miao miao miao" << endl;
    }
    virtual void Accept(IVisitor *vis) {
        vis->visit(this);
    }
};

struct Dog : Animal {
    void say() {
        cout << "wang wang wang" << endl;
    }
    virtual void Accept(IVisitor *vis) {
        vis->visit(this);
    }
};

struct People : Animal {
    void say() {
        cout << "wo ai haizei" << endl;
    }
    virtual void Accept(IVisitor *vis) {
        vis->visit(this);
    }
};

struct Bat : Animal {
    void say() {
        cout << "biu biu biu" << endl;
    }
    virtual void Accept(IVisitor *vis) {
        vis->visit(this);
    }
};

struct OutputVisitor : Animal::IVisitor {
    void visit(Cat *obj) {
        cout << "this is a cat" << endl;
    }
    void visit(Dog *obj) {
        cout << "this is a dog" << endl;
    }
    void visit(People *obj) {
        cout << "this is a person" << endl;
    }
    void visit(Bat *obj) {
        cout << "this is a bat" << endl;
    }
};

struct OutputVisitor2 : Animal::IVisitor {
    void visit(Cat *obj) {
        cout << "1" << endl;
    }
    void visit(Dog *obj) {
        cout << "2" << endl;
    }
    void visit(People *) {
        cout << "3" << endl;
    }
    void visit(Bat *obj) {
        cout << "4" << endl;
    }
};

Animal *getCat() {
    return new Cat;
}

Animal *getDog() {
    return new Dog;
}

Animal *getPeople() {
    return new People;
}

Animal *getBat() {
    return new Bat;
}

Animal *(*getFuncs[4])() = {getCat, getDog, getPeople, getBat};

int main() {
    srand(time(0));
    Animal *arr[20];
    for (int i = 0; i < 20; i++) {
        arr[i] = getFuncs[rand() % 4]();
    }
    for (int i = 0; i < 20; i++) {
        OutputVisitor vis;
        OutputVisitor2 vis2;
        arr[i]->Accept(&vis);
        arr[i]->Accept(&vis2);
    }
    return 0;
}
