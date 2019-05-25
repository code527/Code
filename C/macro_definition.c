/*************************************************************************
	> File Name: macro_definition.c
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 五  2/ 8 22:39:13 2019
 ************************************************************************/
#include <stdio.h>
#include <stdlib.h>

#define MAX(a, b) ({\
    __typeof__(a) __A = (a);\
    __typeof__(b) __B = (b);\
    __A > __B ? __A : __B;\
})

#define Plog(frm, arg...) ({ \
    printf("[ %s : %d ] " frm "\n", __func__, __LINE__, ##arg); \
    fflush(stdout); \
})

void haizei_test() {
    int a = 6;
    Plog("%d", MAX(2, 3));
    Plog("%d", 5 + MAX(2, 3));
    Plog("%d", MAX(2, MAX(3, 4)));
    Plog("%d", MAX(2, 3 > 4 ? 3 : 4));
    Plog("%d", MAX(a++, 6));
    Plog("a value = %d", a);

}

int main() {
    haizei_test();
    return 0;
}
