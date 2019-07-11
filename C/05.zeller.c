/*************************************************************************
	> File Name: zeller.c
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 五  2/ 8 20:56:26 2019
    日一二三四五六
    6 5 4 3 2 1 0
 ************************************************************************/
#include <stdio.h> 
#include <inttypes.h>

int32_t WhichDay(int32_t y, int32_t m, int32_t d) {
    if (m == 1 || m == 2) {
        --y;
        m += 12;
    }
    int32_t w;
    w = (d + 2 * m + 3 * (m + 1) / 5
        + y + y / 4 - y / 100
        + y / 400) % 7;
    return w;
}

int main() {
    int32_t numday = 0, y1, m1, d1, y2, m2, d2;
    scanf("%d%d%d", &y1, &m1, &d1);
    scanf("%d%d%d", &y2, &m2, &d2);
    for (int32_t y = y1; y <= y2; ++y) {
        if (WhichDay(y, 6, 6) == 5)
            ++numday;
    }
    if (WhichDay(y1, 6, 6) == 5 && m1 >= 6 && d1 > 6) --numday;
    if (WhichDay(y2, 6, 6) == 5 && m1 <= 6 && d1 < 6) --numday;
    printf("%d\n", numday);
    return 0;
}
