#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import MySQLdb
import time
import xlsxwriter

#当前环境
ENV_SEL = "QC"

if ENV_SEL == "QA":
    # qa
    MYSQL_URL = "10.250.100.91"
    USER_NAME = "im_rw"
    PASSWORD = "123456"
    SQL_NAME = "immanager"
    USE_PORT = 3308

elif ENV_SEL == "SIM":
    # sim
    MYSQL_URL = "10.250.100.91"
    USER_NAME = "sim_user"
    PASSWORD = "sim_user"
    SQL_NAME = "immanager"
    USE_PORT = 3308

elif ENV_SEL == "QC":
    # online
    MYSQL_URL = "imdb-shard-slave.qc.huohua.cn"
    USER_NAME = "imma_rw"
    PASSWORD = "VyY4a03^rye3pxUI"
    SQL_NAME = "immanager"
    USE_PORT = 3407
else:
    print("ENV SEL ERROR:", ENV_SEL)
 
# 函数功能：连接mysql数据库
def connectMysql():
    db = MySQLdb.connect(MYSQL_URL, USER_NAME, PASSWORD, SQL_NAME, USE_PORT, charset='utf8')
    return db
 
# 函数功能：断开mysql数据库
def disconnectMysql(db):
    db.close()
 
# 函数功能：获取游标
def getCursor(db):
    return db.cursor()
 
# 函数功能：
def learn(db, table, id, start, end):
    cursor = getCursor(db)
    # 执行select sql语句
    sql = "select count(*) from im_messages_" + str(table) +  " where from_user_id=" + str(id)[:-1] + " and msg_type=51 and sent_when between \'" + str(start) + "\' and \'" + str(end) + "\'"
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        count = cursor.fetchone()
        print ("count:", count[0])
        return count
    except:
        return 0

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

if __name__ == "__main__":
    readList = readListFromFile("learn.txt")
    workbook = xlsxwriter.Workbook('./test.xlsx')
    worksheet = workbook.add_worksheet()

    db = connectMysql()
    print(len(readList))

    
    for row in range(len(readList)):
        for col1 in range(14, 16):
            start = "2021-03-"+str(col1 + 16)
            end = "2021-03-"+str(col1 + 17)
            cnt = learn(db, "202103", readList[row], start, end)
            print(cnt)
            if (row == 0):
                worksheet.write_string(row, col1, start)
            worksheet.write_string(row + 1, col1, str(cnt[0]))
        for col2 in range(16, 35):
            tmp = col2 - 16
            if (tmp <= 9):
                start = "2021-04-0"+str(tmp)
                if (tmp == 9):
                    end = "2021-04-" + str(tmp + 1)
                else:
                    end = "2021-04-0" + str(tmp + 1)
            else:
                start = "2021-04-"+str(tmp)
                end = "2021-04-"+str(tmp + 1)
            cnt = learn(db, "202104", readList[row], start, end)
            print(cnt)
            if (row == 0):
                worksheet.write_string(row, col1, start)
            worksheet.write_string(row + 1, col1, str(cnt[0]))
        time.sleep(0.2)
    disconnectMysql(db)
    workbook.close()

