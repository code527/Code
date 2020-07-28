/*************************************************************************
	> File Name: sequence_num.c
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 五  2/ 8 21:50:02 2019
 ************************************************************************/
#include <stdio.h>

int32_t GetDi(int32_t n) {
    if (n <= 9) return n;
    n -= 10;
    int32_t cur = 10, j = 2, num;//j 位数 cur 权
    while (n >= j * (cur * 10 - cur)) {
        n -= j * (cur * 10 - cur);
        cur *= 10;
        j += 1;
    }
    num = n / j + cur;
    for (int32_t i = 0; i < j - n % j - 1; i++) num /= 10;
    return num % 10;
}

int main() {
    int32_t x, y, z, ans = 0;
    scanf("%d%d%d", &x, &y, &z);
    ans = GetDi(x) * GetDi(y) * GetDi(z);
    printf("%d\n", ans);
    return 0;
}
