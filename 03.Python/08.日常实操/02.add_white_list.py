#!/usr/bin/python
# coding:utf-8

import json
import requests

def readIdListFromFile(file):
    fp = open(file, "r+")
    print "文件名为: ", fp.name

    idlist = []
    try:
        while True:
            line = fp.readline()
            # print line
            line = line.strip('\r')
            line = line.strip('\n')
            if len(line) == 0:
                break
            # idlist.add(int(line))
            idlist.append(line)
    finally:
        fp.close()
        print("count:" + str(len(idlist)))

    return idlist

def CRMId2IMId(crmId, type):
    if type > 255 or crmId <= 0:
        return 0

    imid = (int(crmId) << 8) | (type)
    return imid

if __name__ == "__main__":
    url = 'http://10.250.100.93:19501/addwhitelist'
    idlist = readIdListFromFile("00.txt")
    print(idlist)
    for id in idlist:
        imid = CRMId2IMId(id, 1)
        # print(imid)
        postRow = {"traceId":"addwhitelist", "imid":str(imid), "flag":16}
        header_dict = {"Content-Type":"application/json; charset=utf8"}
        rows = json.dumps(postRow)
        # print(rows)
        r = requests.post(url, data=rows, headers=header_dict)
        # print(r.text)



