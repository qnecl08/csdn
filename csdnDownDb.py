import pymysql
import time,datetime
from DBUtils.PooledDB import PooledDB

pool = PooledDB(pymysql,1,host='localhost',user='root',passwd='root',db='daixiazai',port=3306,charset='utf8',cursorclass=pymysql.cursors.DictCursor) #5为连接池里的最少连接数
conn = pool.connection()
cursor=conn.cursor()
def useAccount(score):
    sql="select * from csdn_account where today_download_times<21 and account_type='normal' and score>=%s   order by today_download_times asc limit 0,1"
    cursor.execute(sql,[score])
    accounts=cursor.fetchall()
    if len(accounts)>0:
        pass
    else:
        sql="select * from csdn_account where today_download_times<21 and account_type='vip'  order by today_download_times asc limit 0,1"
        cursor.execute(sql)
        accounts = cursor.fetchall()
        if len(accounts) > 0:
            pass
        else:
            return None
    sql="update csdn_account set today_download_times=today_download_times+1 where account=%s"
    cursor.execute(sql,[accounts[0]['account']])
    return accounts[0]
def hasCanUseAccount():
    sql = "select * from csdn_account where today_download_times<21 order by today_download_times asc limit 0,1"
    cursor.execute(sql)
    accounts = cursor.fetchall()
    if accounts:
        return 1
    else :
        return 0

#更新账号积分
def updateAccountScore(account,score):
    sql="update csdn_account set score=%s where account=%s"
    cursor.execute(sql,[score,account])

#获取最后插入的文件
def lastInsertFile():
    sql="select * from csdn_download order by id DESC limit 0,1"
    cursor.execute(sql)
    files=cursor.fetchall()
    if len(files)>0:
        return files[0]
    else:
        return None
#新下载成功的文件
def insertFile(input):
    sql="insert into csdn_download (file_name,mail,src_url,path,csdn_account,order_no,step,create_time)VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,[input['file_name'],input['mail'],input['src_url'],input['path'],input['csdn_account'],input['order_no'],0,str(int(time.time()))])
    return cursor.lastrowid

if __name__ == "__main__":
   print(useAccount(2))

