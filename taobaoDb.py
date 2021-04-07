import pymysql
import time,datetime
from DBUtils.PooledDB import PooledDB

pool = PooledDB(pymysql,1,host='localhost',user='root',passwd='root',db='daixiazai',port=3306,charset='utf8',cursorclass=pymysql.cursors.DictCursor) #5为连接池里的最少连接数
conn = pool.connection()
cursor=conn.cursor()
def newOrder(order_no,order_type,remark):
    try:
        sql="insert into tb_order (order_no,step,order_type,remark,create_time,update_time) values(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,[order_no,0,order_type,remark,str(int(time.time())),str(int(time.time()))])
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        return 0

def getOrder(order_no):
    sql="select * from tb_order where order_no=%s"
    cursor.execute(sql,[order_no])
    orders=cursor.fetchall()
    if len(orders)==0:
        return None
    else:
        return orders[0]

def notDealOrder():
    sql="select * from tb_order where step='0'"
    cursor.execute(sql)
    orders=cursor.fetchall()
    return orders

def updateStepOrder(order_no,step):
    sql="update tb_order set step=%s,update_time=%s where order_no=%s"
    cursor.execute(sql,[step,int(time.time()),order_no])


if __name__ == "__main__":
    id=newOrder("3322","csdn")
    print(id)
    print(getOrder("3322"))

