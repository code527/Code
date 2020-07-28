/*************************************************************************
	> File Name: leap_year.c
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 五  2/ 8 20:39:17 2019
 ************************************************************************/
# include <stdio.h>
# include <inttypes.h>

int64_t is_leap_year(int64_t n) {
    if ((n % 4 == 0 && n % 100 != 0) || (n % 400 == 0)) {
        return 1;
    } else {
        return 0;
    }
}
int main() {
    int64_t n;
    scanf("%"PRId64, &n);
    if (is_leap_year(n)) {
        printf("L\n");
    } else {
        printf("N\n");
    }
    return 0;
}
