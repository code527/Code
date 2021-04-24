#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import MySQLdb
import time
import json
import xlsxwriter
import sys

reload(sys)
sys.setdefaultencoding( "utf-8" )

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
def learn_refer(db, table, id):
    cursor = getCursor(db)
    # 执行select sql语句
    sql = "select from_user_id, to_user_id, from_type, to_type, session_id, sent_when, content, refer from im_messages_" + str(table) + " where (from_user_id=" + str(id) + " or to_user_id=" + str(id) + ") and msg_type=51 and refer is not null and refer!=\'\'"
    # print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        #content = cursor.fetchone()
        results = cursor.fetchall()
        # print ("count:", count[0])
        return results
    except:
        return 0

# 函数功能：
def learn_refer_session(db, table, session, start):
    cursor = getCursor(db)
    # 执行select sql语句
    sql = "select from_user_id, to_user_id, from_type, to_type, session_id, sent_when, content, refer from im_messages_" + str(table) +  " where session_id=\'" + str(session) + "\' and sent_when > \'" + str(start) + "\'"
    # print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        #content = cursor.fetchone()
        results = cursor.fetchall()
        # print ("count:", count[0])
        return results
    except:
        return 0

# 获取学情类型
def get_mark_type(refer):
    refer = json.loads(refer)
    # print(refer)
    cardinfo = refer["content"]
    # print(cardinfo)
    info = json.loads(cardinfo)
    res = info["content"]
    mark = res["mark"]
    # print(mark)
    return str(mark)

def get_card_info(refer):
    refer = json.loads(refer)
    # print(refer)
    cardinfo = refer["content"]
    # print(cardinfo)
    return str(cardinfo)

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

# 读取文件
def readLListFromFile(file):
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
            readList.append(line.split())
    finally:
        fp.close()
        print("count:" + str(len(readList)))
        # print(readList)

    return readList

# 获取imid
def CRMId2IMId(crmId, type):
    if type > 255 or crmId <= 0:
        return 0

    imid = (int(crmId) << 8) | (type)
    return imid

if __name__ == "__main__":
    title = ['用户ID', 'imid', '辅导老师', '消息来自谁', '消息发给谁', '发送者类型', '接受者类型', '会话ID', '发送时间', '消息内容', '引用消息类型', '引用卡片消息']
    readList = readLListFromFile("learn_refer_content.txt")
    workbook = xlsxwriter.Workbook('./test_refer_content.xlsx')
    worksheet = workbook.add_worksheet()

    db = connectMysql()
    print(len(readList))

    index = 0
    for t in range(len(title)):
        worksheet.write_string(index, t, title[t])
    index += 1
    for row in range(len(readList)):
        print(row)
        imid = CRMId2IMId(int(readList[row][0]), 1)
        refer = learn_refer(db, "202104", imid)
        for i in refer:
            mark = get_mark_type(i[7])
            card = get_card_info(i[7])
            worksheet.write_string(index, 0, readList[row][0])
            worksheet.write_string(index, 1, str(imid))
            worksheet.write_string(index, 2, readList[row][1])
            for col in range(len(title) - 3):
                if col == 7:
                    worksheet.write_string(index, col + 3, mark)
                elif col == 8:
                    worksheet.write_string(index, col + 3, card)
                else:
                    worksheet.write_string(index, col + 3, str(i[col]))
            index += 1
            session = learn_refer_session(db, "202104", i[4], i[5])
            cnt = 0
            for i in session:
                if (cnt >= 5):
                    break
                # worksheet.write_string(index, 0, readList[row][0])
                # worksheet.write_string(index, 1, str(imid))
                # worksheet.write_string(index, 2, readList[row][1])
                for col in range(len(title) - 3):
                    if col == 7:
                        worksheet.write_string(index, col + 3, mark)
                    elif col == 8:
                        worksheet.write_string(index, col + 3, " ")
                    else:
                        worksheet.write_string(index, col + 3, str(i[col]))
                index += 1
                cnt += 1
        time.sleep(0.05)
    disconnectMysql(db)
    workbook.close()

