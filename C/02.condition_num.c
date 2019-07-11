/*************************************************************************
	> File Name: condition_num.c
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 五  2/ 8 21:33:12 2019
 ************************************************************************/
#include <stdio.h> 
#include <inttypes.h>
#define MAX_N 10

int dnum[MAX_N + 5] = {0};
int jnum[MAX_N + 5] = {0};

void init() {
    jnum[0] = 1;
    for (int i = 1; i < MAX_N; i++) {
        dnum[i] = 1;
        jnum[i] = i * jnum[i - 1];
    }
    return ;
}

int get_num(int n, int k) {
    int ind = (k / jnum[n]) + 1, i = -1;
    while (ind > 0) {
        i++;
        ind -= dnum[i];
    }
    dnum[i] = 0;
    return i;
}

int main() {
    init();
    int n, k;
    scanf("%d%d", &n, &k);
    k -= 1;
    for (int i = n - 1; i >= 0; i--) {
        int num = get_num(i, k);
        printf("%d", num);
        k %= jnum[i];
    }
    printf("\n");
    return 0;
}
