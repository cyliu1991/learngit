# !/usr/local/bin/python3

# coding=utf-8
import pymysql
import json
import requests
import re
from sshtunnel import SSHTunnelForwarder
import testcases.doneExercise.def_func as done_exercise_func
import testcases.exerciseResults.def_func as exercise_result_func
import time

########################################
# For test suite
########################################
global file_path
file_path = 'conf.json'


# initialization
def get_base_url():
    with open(file_path) as conf_fp:
        res = json.load(conf_fp)
    return(res["base_url"])


def get_username():
    with open(file_path) as conf_fp:
        res = json.load(conf_fp)
    return(res["phoneNumber"])


def get_password():
    with open(file_path) as conf_fp:
        res = json.load(conf_fp)
    return(res["password"])


# get token
def get_token():
    base_url = get_base_url()
    phone_number = get_username()
    password = get_password()
    login_url = base_url + "/student/login/login"
    data = {"phoneNumber": phone_number,
            "password": password}
    res = requests.post(url=login_url, json=data)
    pattern = r'"token":"(.*?)"'
    p_token = re.compile(pattern)
    token = re.findall(p_token, res.text)
    return token[0]


def get_student_id():
    with open(file_path) as conf_fp:
        res = json.load(conf_fp)
    return(res["student_id"])



def create_conn():
    server =  SSHTunnelForwarder(
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


def remove_conn(server,conn):
    conn.close()
    server.close()


#####################################
# doneExcerciseList
#####################################
def create_doneExerciseList(student_id):
    (server, conn) = create_conn()
    doneExerciseList = done_exercise_func.create_done_exercise_list(conn, student_id)
    remove_conn(server, conn)
    return doneExerciseList


def get_last_page_num(exercise_list, limit):
    last_page = done_exercise_func.get_last_page(exercise_list, limit)
    return last_page


def get_doneExercise_num(exercise_list):
    done_exercise_num = done_exercise_func.get_doneExercise_num(exercise_list)
    print("done_exercise_num:", done_exercise_num)
    return str(done_exercise_num)


def get_page_doneExerciseList(exercise_list, mode, page, limit):
    if mode == 0:
        page_list = done_exercise_func.get_doneExerciseList_timeDecrease(exercise_list, page, limit)
    else:
        page_list = done_exercise_func.get_doneExerciseList_timeIncrease(exercise_list, page, limit)
    return page_list


###################################
#exerciseResults
###################################
def get_exercise_paperID():
    exercise_paperID = exercise_result_func.get_exercise_paperID()
    return exercise_paperID


if __name__ == '__main__':
    (server, conn) = create_conn()
#    create_time = time.strftime("%Y-%m-%d %X", time.localtime())
#    end_time = time.strftime("%Y-%m-%d %X", time.localtime())
    done_exercise_func.create_done_exercise_list(conn, '0101010011302023')

#    conn.commit()
    conn.close()
    server.close()
