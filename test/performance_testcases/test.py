import aiohttp
import asyncio
from base import base as base
import utils.make_exercise as make_exercise
import os
import json
import time


# 创建测试用户
def create_user(cursor, num):
    print("Creating users and exercise ......")
    password = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    sql_insert_user_info = "INSERT INTO `testeducation`.`student_info`(`student_id`, `user_name`, `password`, `picture_path`) " \
          "VALUES ('%s', '%s', '%s', NULL)"
    sql_insert_student_info = "INSERT INTO `testeducation`.`student`(`student_id`, `student_name`, `student_gender`, `student_gender_chinese`, `student_birthday`, `student_grade`, `student_semester`, `student_unit`, `class_id`, `grade_id`, `school_id`, `textbook_id`, `student_graduate`) " \
           "VALUES ('%s', '%s', 1, '男', '2012-04-07', 1, '1.1', '1.1.08', '0101010011802', '01010100118', '010101001', 'A1', 0)"
    question_id_list = ['0101010003001004', '0101010003001014', '0101010003001020',
                        '0101010003001021', '0101010003001025', '0101010003001059',
                        '0101010003001050', '0101010003001046',
                        '0101010005001009', '0101010005001011']
    users_file = '../data/users.txt'
    with open(users_file, 'a+') as fp:
        for i in range(1, num+1):
            student_id = "155%08d" % i
            user_name = "155%08d" % i
            fp.write(user_name+',')
            testpaper_id = "155%08d-1" % i
            # 判断学生是否已存在，若已存在，继续下一条数据插入
            cursor.execute("select * from student_info where user_name='%s'" % user_name)
            if cursor.fetchone():
                continue
            #     cursor.execute("delete from student_info where user_name='%s'" % user_name)
            # cursor.execute("select * from student where student_name='%s'" % user_name)
            # if cursor.fetchone():
            #     cursor.execute("delete from student where student_name='%s'" % user_name)

            # 向student_info、student中插入学生信息
            cursor.execute(sql_insert_user_info % (student_id, user_name, password))
            cursor.execute(sql_insert_student_info % (student_id, user_name))
            make_exercise.make_exercise(cursor, user_name, question_id_list, testpaper_id)
        print("Creating users and exercise finished.")
        return users_file


# 获取请求数据
def get_student_request_datas(username=None, exercise_id=None, question_id=None, start_time=None, end_time=None):
    request_datas = {
        "login": {"method": "POST", "url": "https://test2.data4truth.com/student/login/login",
                  "data": {"phoneNumber": username, "password": "123456"}},
        "getExercise": {"method": "GET", "url": "https://test2.data4truth.com/student/practice/getExercise",
                        "data": None},
        "getQuestion": {"method": "GET", "url": "https://test2.data4truth.com/student/practice/getQuestion",
                        "data": {"exerciseID": exercise_id}},
        "submitExercise": {"method": "POST", "url": "https://test2.data4truth.com/student/practice/submitExercise",
                           "data": {
                                    "answerList": [{"questionID": question_id, "answer": "test",
                                                    "exerciseStart": start_time, "exerciseEnd": end_time}],
                           "exerciseID": exercise_id}},
        "logout": {"method": "POST", "url": "https://test2.data4truth.com/student/login/logout", "data": None}
    }
    return request_datas


def get_login_data(username, password="123456"):
    login_data = {"method": "POST", "url": "https://test2.data4truth.com/student/login/login",
                  "data": {"phoneNumber": username, "password": password}}
    return login_data


def get_test_question_data(test_id, start_time, end_time, number, is_test, question_id):
    test_question_data = {"method": "GET", "url": "https://test2.data4truth.com/student/test/getQuestion",
                          "data": {"gradeID": "6.2",
                                   "unitID": "6.2.05",
                                   "testID": test_id,
                                   "questionID": question_id,
                                   "answer": "test",
                                   "startTime": start_time,
                                   "endTime": end_time,
                                   "number": number,
                                   "isTest": is_test}}
    return test_question_data


def get_test_grade_data():
    test_grade_data = {"method": "GET", "url": "https://test2.data4truth.com/student/test/selectGrade",
                       "data": {"gradeID": "6.2"}}
    return test_grade_data


def get_logout_data():
    logout_data = {"method": "POST", "url": "https://test2.data4truth.com/student/login/logout", "data": None}
    return logout_data


def get_exercise_id():
    pass


def get_question_id():
    pass


def setup(user_num):
    print("Preparing for testing data ...... ")
    (server, conn) = base.create_conn()
    with conn.cursor() as cursor:
        try:
            create_user(cursor, user_num)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            server.close()
    print("Preparing for testing data finished.")


async def fetch(session, method, url, data=None, headers=None):

    if method == 'GET':
        async with session.get(url, params=data, headers=headers) as resp:
            res_content = await resp.text()
            print("text：", res_content)
    else:
        async with session.post(url, json=data, headers=headers) as resp:
            res_content = await resp.text()
            print("text：", res_content)
    return res_content


async def login(session, username):
    login_data = get_login_data(username)
    url = login_data["url"]
    data = login_data["data"]
    print("url:", url)
    try:
        res_content = await fetch(session, method='POST', url=url, data=data)
        res_json = json.loads(res_content)
        token = res_json["data"]["token"]
        print(username, ':', token)
    except Exception as e:
        raise e
    return token
    # print("token:", token)


# 获取练习题列表
async def get_exercise(session, headers):
    request_data = get_student_request_datas()["getExercise"]
    method = request_data["method"]
    url = request_data["url"]
    print("url:", url)
    data = request_data["data"]
    await fetch(session, method, url, data=data, headers=headers)


# 获取练习题题目
async def get_question(session, headers, exercise_id):
    request_data = get_student_request_datas(exercise_id=exercise_id)["getQuestion"]
    method = request_data["method"]
    url = request_data["url"]
    print("url:", url)
    data = request_data["data"]
    await fetch(session, method, url, data=data, headers=headers)


# 做练习题,提交一道题目做题结果
async def submit_question(session, headers, exercise_id, question_id):
    start_time = time.strftime("%Y-%m-%d %X", session.loop.time())
    await asyncio.sleep(1)
    end_time = time.strftime("%Y-%m-%d %X", session.loop.time())
    request_data = get_student_request_datas(exercise_id=exercise_id, question_id=question_id,
                                             start_time=start_time, end_time=end_time)["getExercise"]
    method = request_data["method"]
    url = request_data["url"]
    data = request_data["data"]
    print("url:", url)
    await fetch(session, method, url, data=data, headers=headers)


# 提交整套练习题
async def submit_exercise(session, headers, exercise_id, question_list):
    for question_id in question_list:
        await submit_question(session, headers, exercise_id, question_id)


# 获取知识测评年级
async def test_select_grade(session, headers):
    test_grade_data = get_test_grade_data()
    method = test_grade_data["method"]
    # print("method", method)
    url = test_grade_data["url"]
    print("url:", url)
    data = test_grade_data["data"]
    # print("data:", data)
    res_content = await fetch(session, method=method, url=url, headers=headers, data=data)
    res_json = json.loads(res_content)
    # assert res_json["code"] == 10000
    print(res_json)
    return res_json


# 知识测评获取题目
async def get_test_question(session, headers, test_question_data, username):
    method = test_question_data["method"]
    url = test_question_data["url"]
    data = test_question_data["data"]
    print(username, "-url:", url)
    res_context = await fetch(session, method=method, url=url, headers=headers, data=data)
    res_json = json.loads(res_context)
    return res_json


# 进行知识测评
async def knowlege_test(session, headers, select_grade_res, username):
    test_id = select_grade_res["data"]["unitList"][0]["testID"]
    start_time = base.local_time()
    end_time = base.local_time()
    number = 0
    is_test = select_grade_res["data"]["unitList"][0]["isTest"]
    test_question_data = {
        "method": "GET", "url": "https://test2.data4truth.com/student/test/getQuestion",
        "data": {"gradeID": "6.2",
                 "unitID": "6.2.05",
                 "testID": test_id,
                 "answer": "test",
                 "startTime": start_time,
                 "endTime": end_time,
                 "number": number,
                 "isTest": is_test}}

    while number < 5:
        test_question_res = await get_test_question(session, headers, test_question_data, username)
        number += 1
        test_question_data["data"]["number"] = number
        test_question_data["questionID"] = test_question_res["data"]["questionList"][0]["questionID"]


# 登出
async def logout(session, headers):
    logout_data = get_student_request_datas()["logout"]
    method = logout_data["method"]
    url = logout_data["url"]
    print("url:", url)
    await fetch(session, method=method, url=url, headers=headers)


async def on_request_start(session, trace_config_ctx, params):
    trace_config_ctx.start = session.loop.time()


async def on_request_end(session, trace_config_ctx, params):
    elapsed = session.loop.time() - trace_config_ctx.start
#    print("Request took {}".format(elapsed), params)
    with open("../data/elapsed.txt", 'a+') as fp:
        fp.write("{'url':'" + str(params.url) + "', 'elapsed':" + str(elapsed)+"},")


# 定义用户行为
async def user_tasks(username):
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)
    async with aiohttp.ClientSession(
                                     trace_configs=[trace_config], connector=aiohttp.TCPConnector(ssl=False)) as session:
        # exercise_id = str(username) + '-1'
        # question_list = ['0101010003001004', '0101010003001014', '0101010003001020',
        #                  '0101010003001021', '0101010003001025', '0101010003001059',
        #                  '0101010003001050', '0101010003001046',
        #                  '0101010005001009', '0101010005001011']
        token = await login(session, username)
        print("token:", token)
        headers = {"token": token}
        select_grade_res = await test_select_grade(session, headers)
        print("res:", select_grade_res)
        await knowlege_test(session, headers=headers, select_grade_res=select_grade_res, username=username)


        # await get_exercise(session, headers=headers)
        # await get_question(session, headers=headers, exercise_id=exercise_id)
        # await submit_exercise(headers, exercise_id, question_list)
        await logout(session, headers)


async def users_concurrent(users_file='../data/users.txt'):
    with open(users_file, 'r') as fp:
        users = eval(fp.read())
    tasks = []
    for user in users:
        tasks.append(asyncio.create_task(user_tasks(user)))
    await asyncio.wait(tasks)


# 获取练习题做题结果
def get_exercise_results():
    pass


# 运行测试脚本
def run_test():
    asyncio.run(users_concurrent())


# 统计指定url平均请求时间
def count_elapsed(url, file_name):
    sum_elapsed_time = 0
    request_times = 0
    with open(file_name) as fp:
        elapsed_datas = eval(fp.read())
    for elapsed_data in elapsed_datas:
        if elapsed_data["url"] == url:
            print(elapsed_data["url"], elapsed_data["elapsed"])
            request_times += 1
            sum_elapsed_time += elapsed_data["elapsed"]
    avg_elapsed = sum_elapsed_time/request_times
    return avg_elapsed


# 生成请求时间统计报告
def make_elapsed_report(file_name='../data/elapsed.txt'):
    url_list = [
        "https://test2.data4truth.com/student/login/login",
        "https://test2.data4truth.com/student/test/selectGrade",
        "https://test2.data4truth.com/student/test/getQuestion",
        "https://test2.data4truth.com/student/login/logout"
    ]
    with open('../report/elapsed.report', 'a+') as fp:
        for url in url_list:
            url_avg_elapsed = count_elapsed(url, file_name)
            fp.write(url + ":" + str(url_avg_elapsed)+'\n')


def main():
    user_num = 200
    user_file_path = '../data/users.txt'
    if not os.path.exists(user_file_path):
        setup(user_num)

    with open(user_file_path, 'r') as fp:
        users = eval(fp.read())
    if len(users) == user_num:
        run_test()
    else:
        os.remove(user_file_path)
        setup(user_num)
        run_test()


if __name__ == '__main__':
    start_time = time.time()
    while time.time()-start_time < 1000:
        main()
    make_elapsed_report()



