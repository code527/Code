/*************************************************************************
	> File Name: 08.hashtable.h
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 四  7/11 15:29:26 2019
 ************************************************************************/

#ifndef _08.HASHTABLE_H
#define _08.HASHTABLE_H

typedef int (*HashFuncRaw)(const void *value);

class HashFunc {
public :
    virtual int operator()(const void *value) = 0;
    virtual ~HashFunc() {}
};

class HashTable {
public :
    HashTable(HashFunc &hc) : __hc(&hc), __hcr(nullptr) {}
    HashTable(HashFuncRaw hc) : __hcr(hc), __hc(nullptr) {}
    int get_hash(const void *data) {
        if (this->__hc) {
            return (*(this->__hc))(data);
        } else {
            return this->__hcr(data);
        }
    }
private :
    HashFunc *__hc;
    HashFuncRaw __hcr;
};

#endif
