#!/usr/bin/env python
# coding=utf-8

import sys


# 读取文件
def readListFromFile(file):
    fp = open(file, "r+")
    print ("文件名为: ", fp.name)

    readList = []
    try:
        while True:
            line = fp.readline()
            line = line.strip('\r')
            line = line.strip('\n')
            if len(line) == 0:
                break
            readList.append(line)
    finally:
        fp.close()
        print("count:" + str(len(readList)))

    return readList

if __name__ == "__main__":
    readList = readListFromFile("sum.txt")
    cnt = 0
    for i in readList:
        cnt += int(i)
    print(cnt)
