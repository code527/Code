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
    sql = "select count(*) from im_messages_" + str(table) +  " where (from_user_id=" + str(id) + " or to_user_id=" + str(id) + ") and msg_type=51 and  refer is not null and refer!=\'\'" + " and sent_when >= \'" + str(start) + "\' and sent_when < \'" + str(end) + "\'"
    #print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        count = cursor.fetchone()
        #print ("count:", count[0])
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
    workbook = xlsxwriter.Workbook('./test_refer.xlsx')
    worksheet = workbook.add_worksheet()

    db = connectMysql()
    print(len(readList))

    for col in range(52):
        count = 0
        for row in range(len(readList)):
            imid = CRMId2IMId(int(readList[row]), 1)
            if (col == 0 and row == 0):
                worksheet.write_string(row, col, "sum")
            elif (col != 0 and row == 0):
                if (col >= 1 and col <= 31):
                    if (col <= 9):
                        title = "2021-03-0" + str(col)
                        if (col == 9):
                            end = "2021-03-" + str(col + 1)
                    else:
                        title = "2021-03-" + str(col)
                else:
                    tmp = col - 31
                    if (tmp <= 9):
                        title = "2021-04-0"+str(tmp)
                        if (tmp == 9):
                            end = "2021-04-"+str(tmp + 1)
                    else:
                        title = "2021-04-"+str(tmp)
                print(title)
                worksheet.write_string(row, col, title)
            else:
                if (col >= 1 and col <= 31):
                    if (col <= 9):
                        start = "2021-03-0" + str(col)
                        if (col == 9):
                            end = "2021-03-" + str(col + 1)
                        else:
                            end = "2021-03-0" + str(col + 1)
                    else:
                        start = "2021-03-" + str(col)
                        end = "2021-03-" + str(col + 1)
                    cnt = learn(db, "202103", imid, start, end)
                    count += int(cnt[0])
                elif (col > 31):
                    tmp = col - 31
                    if (tmp <= 9):
                        start = "2021-04-0"+str(tmp)
                        if (tmp == 9):
                            end = "2021-04-"+str(tmp + 1)
                        else:
                            end = "2021-04-0"+str(tmp + 1)
                    else:
                        start = "2021-04-"+str(tmp)
                        end = "2021-04-"+str(tmp + 1)
                    cnt = learn(db, "202104", imid, start, end)
                    count += int(cnt[0])
                worksheet.write_string(row, col, str(count))
        print(count)
        time.sleep(0.01)
    disconnectMysql(db)
    workbook.close()

