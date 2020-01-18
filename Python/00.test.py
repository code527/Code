#!/usr/bin/env python
# coding=utf-8

def is_prime(x):

    if type(x) != type(1):

        return False

    for i in xrange(2, x):

        if x % i == 0:

            break

    else :

        return True

    return False

while 1:
    a = int(raw_input())
    if a == 0:
        print('bye bye')
        break
    elif is_prime(a):
        print('yes')
    else:
        print('no')
