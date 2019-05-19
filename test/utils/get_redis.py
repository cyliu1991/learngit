# coding=utf-8
import pymysql
import redis
from sshtunnel import SSHTunnelForwarder

server1 = SSHTunnelForwarder(
    '61.174.255.246',  # B机器的配置
    ssh_password='Data4truth.com',
    ssh_username='root',
    remote_bind_address=('10.70.11.215', 3306)  # 数据库服务器配置
)
server1.start()

conn = pymysql.connect(

    host='127.0.0.1',
    port=server1.local_bind_port,
    user='edutest',
    password='Data4truth.com',
    database='testeducation',
)
with conn.cursor() as cursor:
    cursor.execute("SELECT point_unit FROM `point_textbook` group by point_unit")
    res = cursor.fetchall()
conn.close()
server1.close()

server2 = SSHTunnelForwarder(
    '61.174.255.246',  # B机器的配置
    ssh_password='Data4truth.com',
    ssh_username='root',
    remote_bind_address=('10.70.11.77', 13981)  # 数据库服务器配置
)
server2.start()
r = redis.Redis(
    host='127.0.0.1',
    port=server2.local_bind_port,
    password='Redis@123'
)


for unit in res:
    res1 = r.get("QA-A1-%s-candidate-questions" % unit[0])
    print(unit[0], res1)

server2.close()

