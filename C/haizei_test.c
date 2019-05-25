/*************************************************************************
	> File Name: haizei_test.c
	> Author: zhengdongqi
	> Mail: 
	> Created Time: 五  2/ 8 22:48:36 2019
 ************************************************************************/

#include <stdio.h>
#include <inttypes.h>

typedef struct TEST_INFO {
    int testNum;
    int YesNum;
    int NoNum;
} TEST_INFO;

#define TEST(a, b)\
    void a##_haizeix_##b(struct TEST_INFO *); \
    __attribute__((constructor)) \
    void ADDFUNC_##a##_haizeix_##b() { \
        haizei_test_run(a##_haizeix_##b, #a, #b); \
    } \
    void a##_haizeix_##b(struct TEST_INFO *__ti)

#define EXPECT_EQ(a, b) { \
    (a) == (b) ? __ti->YesNum++ : __ti->NoNum++; \
    __ti->testNum++; \
}

int haizei_test_run(void (*func)(TEST_INFO *), const char *str1, const char *str2) {
    TEST_INFO ti = {0, 0, 0};
    printf("[RUN] %s.%s\n", str1, str2);
    func(&ti);
    if (ti.NoNum == 0) {
        printf("[OK] %s.%s %d pass %d failed\n", 
            str1, str2, ti.YesNum, ti.NoNum);
    } else {
        printf("[FAILED] %s.%s %d pass %d failed\n",
            str1, str2, ti.YesNum, ti.NoNum);
    }
    return 0;
}

int isPrime(int x);

TEST(isPrime, bound) {
    EXPECT_EQ(isPrime(0), 0);
    EXPECT_EQ(isPrime(1), 0);
    EXPECT_EQ(isPrime(INT32_MIN), 0);
}

TEST(isPrime, okTest) {
    #ifndef MAX_N
    #define MAX_N 100
    #endif
    int prime[MAX_N + 5] = {1, 1};
    for (int i = 2; i * i <= MAX_N; i++) {
        if (!prime[i]) {
            for (int j = i * i; j <= MAX_N; j += i) {
                prime[j] = 1;
            }
        }
    }
    for (int i = 2; i <= MAX_N; i++) {
        EXPECT_EQ(isPrime(i), prime[i] == 0);
    }
}

TEST(isPrime, failedTest) {
    #ifndef MAX_N
    #define MAX_N 100
    #endif
    int prime[MAX_N + 5] = {1, 1};
    for (int i = 2; i * i <= MAX_N; i++) {
        if (!prime[i]) {
            for (int j = i * i; j <= MAX_N; j += i) {
                prime[j] = 1;
            }
        }
    }
    for (int i = 2; i <= MAX_N; i++) {
        EXPECT_EQ(isPrime(i), prime[i] == 1);
    }
}

int main() {
    return 0;
}

int isPrime(int x) {
    if (x <= 1) return 0;
    for (int i = 2; i * i <= x; i++) {
        if (x % i == 0) return 0;
    }
    return 1;
}

