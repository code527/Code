/*************************************************************************
	> File Name: factor_sum.c
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 五  2/ 8 20:48:41 2019
 ************************************************************************/
#include <stdio.h>
#include <inttypes.h>
#include <math.h>
#define MAX_N 1000000

int prime[MAX_N + 5] = {0};
int pnum[MAX_N + 5] = {0};
int fnum[MAX_N + 5] = {0};
int dnum[MAX_N + 5] = {0};

void init() {
    for (int i = 2; i <= MAX_N; i++) {
        if (!prime[i]) {
            prime[++prime[0]] = i;
            pnum[i] = 1;
            fnum[i] = 2;
            dnum[i] = i + 1;
        }
        for (int j = 1; j <= prime[0] && prime[j] * i <= MAX_N; j++) {
            prime[prime[j] * i] = 1;
            if (i % prime[j] == 0) {
                pnum[prime[j] * i] = pnum[i] + 1;
                fnum[prime[j] * i] = fnum[i] / (pnum[i] + 1) * (pnum[i] + 2);
                dnum[prime[j] * i] = dnum[i] / (pow(prime[j], pnum[i] + 1) - 1) *
                (pow(prime[j], pnum[i] + 2) - 1);
            } else {
                pnum[prime[j] * i] = 1;
                fnum[prime[j] * i] = fnum[prime[j]] * fnum[i];
                dnum[prime[j] * i] = dnum[prime[j]] * dnum[i];
            }
        }
    }
    /*for (int i = 1; i <= MAX_N; i++) {
        dnum[i] -= i;
    }*/
    return ;
}
int main() {
    init();
    int max = 0;
    for (int i = 1; i <= MAX_N; i++) {
        if(max < dnum[i]) {
            max = dnum[i];
        }
    }
    printf("%d\n", max);
    return 0;
}
