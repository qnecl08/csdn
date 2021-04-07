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
        return accounts[0]
    else:
        sql="select * from csdn_account where today_download_times<21 and account_type='vip'  order by today_download_times asc limit 0,1"
        cursor.execute(sql)
        accounts = cursor.fetchall()
        if len(accounts) > 0:
            return accounts[0]
        else:
            return None
def hasCanUseAccount():
    sql = "select * from csdn_account where today_download_times<21 order by today_download_times asc limit 0,1"
    cursor.execute(sql)
    accounts = cursor.fetchall()
    if accounts:
        return 1
    else :
        return 0

def updateAccountScore(account,score):
    sql="update csdn_account set score=%s where account=%s"
    cursor.execute(sql,[score,account])

if __name__ == "__main__":
   print(useAccount(2))

