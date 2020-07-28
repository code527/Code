/*************************************************************************
	> File Name: va_func.c
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 五  2/ 8 22:43:35 2019
 ************************************************************************/

#include <stdio.h>
#include <stdarg.h>

#define Plog(frm, arg...) { \
    printf("[ %s : %d -> output ] " frm "\n", __func__, __LINE__, ##arg); \
    fflush(stdout); \
}

int sum(int n, ...);

void haizei_test() {
    Plog("%d", sum(2, 1, 3));
    Plog("%d", sum(2, 2, 4));
    Plog("%d", sum(10, 5, 3, 6, 9, 10, 11, 1998, 10287, 987, 18713));
    Plog("%d", sum(3, 1, 9, 8, 7, 4));
}

int main() {
    haizei_test();
    return 0;
}

int sum(int n, ...) {
    va_list arg;
    int temp = 0;
    va_start(arg, n);
    for (int i = 1; i <= n; i++) {
        temp += va_arg(arg, int);
    }
    va_end(arg);
    return temp;
}

