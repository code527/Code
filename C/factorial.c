/*************************************************************************
	> File Name: factorial.c
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 五  2/ 8 20:51:33 2019
 ************************************************************************/

#include <stdio.h>
#include <inttypes.h>
#include <math.h>
#define MAX_N 500
#define BASE 10

int64_t arr[MAX_N + 5] = {0};

void init(int n) {
    arr[0] = arr[1] = 1;
    for (int i = 1; i <= n; i++) {
        for (int64_t j = 1; j <= arr[0]; j++) arr[j] *= i;
        for (int64_t k = 1; k <= arr[0]; k++) {
            if (arr[k] < BASE) continue;
            arr[k + 1] += arr[k] / BASE;
            arr[k] %= BASE;
            arr[0] += (arr[0] == k);
        }
    }
    return ;
}

int main() {
    int x;
    while (scanf("%d", &x) != EOF) {
        int64_t sum = 1;
        init(x);
        for (int i = arr[0]; i >= 1; i--) {
            if (arr[i]) {
                sum *= arr[i];
                arr[i] = 0;
            }
        }
        printf("%"PRId64"\n", sum);
    }
    return 0;
}
