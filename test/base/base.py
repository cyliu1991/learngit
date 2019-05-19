# coding=utf-8
from sshtunnel import SSHTunnelForwarder
import pymysql
import requests
import re
import time
import json


def create_conn():
    server = SSHTunnelForwarder(
            '61.174.255.246',  # B机器的配置
            ssh_password='Data4truth.com',
            ssh_username='root',
            remote_bind_address=('10.70.11.215', 3306)  # 数据库服务器配置
    )
    server.start()
#    print(server.local_bind_port)
    conn = pymysql.connect(

        host='127.0.0.1',
        port=server.local_bind_port,
        user='edutest',
        password='Data4truth.com',
        database='testeducation',
    )
    return (server, conn)


def re_findall(pattern, text):
    re_object = re.compile(pattern)
    results = re.findall(re_object, text)
    return results


def re_match(pattern, text):
    re_object = re.compile(pattern)
    flag = re.match(re_object, text)
    return flag


def get_token(login_url='https://test2.data4truth.com/student/login/login', username='17601006087', password='123456'):
    data = {"phoneNumber": username,
            "password": password}
    res = requests.post(url=login_url, json=data, verify=False)
    res_json = json.loads(res.content)
    # print(type(res_json))
    token = res_json["data"]["token"]
    return token


def remove_token():
    pass


def local_time():
    time1 = time.strftime("%Y-%m-%d %X", time.localtime())
    time.sleep(1)
    return time1


def local_date():
    local_data = time.strftime("%Y-%m-%d", time.localtime())
    return local_data


if __name__ == '__main__':
    # (server, conn) = create_conn()
    # with conn.cursor() as cursor:
    #     cursor.execute("SELECT point_unit FROM `point_textbook` GROUP BY point_unit")
    #     res = cursor.fetchall()
    # conn.close()
    # server.close()
    # with open("unit_id.csv", 'a+')  as fp:
    #     for unit_id in res:
    #         fp.write(unit_id[0]+'\n')
    get_token()
