#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import json
import redis
import requests

#当前环境
ENV_SEL = "QA"
filename = "la.txt"

if ENV_SEL == "QA":
    # qa
    REDIS_HOST = 'redis.qa.huohua.cn'
    REDIS_PWD = 'AcUVeRb8lN'
    REDIS_INDEX = 15
    IMHTTP_URL = 'http://10.250.200.198:9090'
    IMHTTP_URL = 'http://imservice.qa.huohua.cn'
    CRM_URL = "http://manage.qa.huohua.cn/"
    LA_URL = "http://crm.qa.huohua.cn"
    RELATION_URL = "http://la-gate.qa.huohua.cn/ai/operator/user/relation"

elif ENV_SEL == "SIM":
    # sim
    REDIS_HOST = 'redis.sim.huohua.cn'
    REDIS_PWD = 'AcUVeRb8lN'
    REDIS_INDEX = 13
    IMHTTP_URL = 'http://10.250.100.93:9090'
    CRM_URL = "http://manage.sim.huohua.cn/"
    LA_URL = "http://crmv2.sim.huohua.cn/api"
    RELATION_URL = "http://la-gate.sim.huohua.cn/ai/operator/user/relation"

elif ENV_SEL == "QC":
    # online
    REDIS_HOST = 'imredis.qc.huohua.cn'
    REDIS_PWD = 'QN!GODRt'
    REDIS_INDEX = 0
    IMHTTP_URL = 'http://imservice.huohua.cn'
    CRM_URL = "http://manage.huohua.cn/"
    LA_URL = "http://crm.huohua.cn"
    RELATION_URL = "http://la-gate.qc.huohua.cn/ai/operator/user/relation"
else:
    print("ENV SEL ERROR:", ENV_SEL)

# redis 连接池
pool = redis.ConnectionPool(host=REDIS_HOST, port=6379, db=REDIS_INDEX, password=REDIS_PWD, decode_responses=True)
r = redis.Redis(connection_pool=pool)

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

# 获取imid
def CRMId2IMId(crmId, type):
    if type > 255 or crmId <= 0:
        return 0

    imid = (int(crmId) << 8) | (type)
    return imid

# 读取相应la的所有会话
def checkSession(id):
    with open(filename, "a+") as f:
        name = "sessionOfUserId:" + str(id)
        zset = r.zrange(name, 0, -1, withscores=True, desc=True)
        for key, value in zset:
            flag = str(key).split("_")
            if flag[0] == "LP":
                if flag[2] == str(id) or flag[3] == str(id):
                    continue
                else:
                    save = "key: %s, score: %.f\n" %(str(key), value)
                    f.write(save)
            if flag[0] == "BZ":
                if flag[1] == str(id) or flag[2] == str(id):
                    continue
                else:
                    save = "key: %s, score: %.f\n" %(str(key), value)
                    f.write(save)

if __name__ == "__main__":
    readList = readListFromFile("00.txt")
    for i in readList:
        imid = CRMId2IMId(i, 2)
        checkSession(imid)
        time.sleep(0.1)
