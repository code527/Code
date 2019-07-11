/*************************************************************************
	> File Name: newton_method.c
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 五  2/ 8 22:46:18 2019
 ************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <assert.h>

#define EPSLON 1e-6
#define sqrt(a) (0)

#define Plog(frm, arg...) { \
    printf("[ %s : %d -> output ] " frm "\n", __func__, __LINE__, ##arg); \
    fflush(stdout); \
}

double newton_sqrt(double n);

void haizei_test() {
    for (int i = 0; i < 1000; i++) {
        double n = rand() % 1000000;
        double x = newton_sqrt(n);
        assert(fabs(x * x - n) < EPSLON);
        Plog("Accept");
    }
    return ;
}

int main() {
    srand(time(0));
    haizei_test();
    return 0;
}

double newton_sqrt(double n) {
    double x = 1.0;
    while(fabs(x * x - n) > EPSLON) {
        x -= (x * x - n) / (2 * x);
    }
    return x;
}

