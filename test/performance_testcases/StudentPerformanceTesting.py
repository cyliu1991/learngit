import aiohttp
import asyncio
from base import base as base
import time
import utils.make_exercise as make_exercise
import re


# 获取测试用户token，供并发测试使用
def get_users_token():
    with open('../data/users.txt', 'r') as fp:
        user_names = eval(fp.read())
        print(user_names)
    tokens = []
    for user_name in user_names:
        print(user_name)
        token = base.get_token(username=user_name)
        tokens.append(token)
    print(tokens)
    return tokens


# 将token写入headers
def get_users_headers():
    tokens = get_users_token()
    headers = []
    for token in tokens:
        header = {"token": token}
        headers.append(header)
    return headers


# 获取请求数据
def get_request_datas(exercise_id=None, question_id=None, start_time=None, end_time=None):
    request_datas = {
        "getExercise": {"method": "GET", "url": "https://test2.data4truth.com/student/practice/getExercise",
                        "data": None},
        "getQuestion": {"method": "GET", "url": "https://test2.data4truth.com/student/practice/getQuestion",
                        "data": {"exerciseID": exercise_id}},
        "submitExercise": {"method": "POST", "url": "https://test2:data4truth.com/student/practice/submitExercise",
                           "data": {
                                    "answerList": [{"questionID": question_id, "answer": "test",
                                                    "exerciseStart": start_time, "exerciseEnd": end_time}],
                            "exerciseID": exercise_id}},
        "logout": {"method": "POST", "url": "https://test2.data4truth.com/student/login/logout",
                   "data": None}
    }
    return request_datas


def get_exercise_id():
    pass


def get_question_id():
    pass


def do_exercise(exercise_id):
    pass


async def on_request_start(session, trace_config_ctx, params):
    trace_config_ctx.start = session.loop.time()
#    print("start_time:", trace_config_ctx.start)
    # star_time = time.time()
    # print("Starting request:", star_time)


async def on_request_end(session, trace_config_ctx, params):
    elapsed = session.loop.time() - trace_config_ctx.start
#    print("Request took {}".format(elapsed), params)
    local_date = base.local_date()
    with open("../data/request_data-%s.txt" % local_date, 'a+') as fp:
        fp.write(str(params) + ', elapsed:' + str(elapsed)+'\n')
        # fp.write(str(elapsed))


    # end_time = time.time()
    # print("Ending request:", end_time)


async def fetch(method, url, data=None, headers=None):
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False), trace_configs=[trace_config]) as session:
        if method == 'GET':
            async with session.get(url, params=data, headers=headers) as resp:
                # json = await resp.json()
                text = await resp.read()
                print("text：", text)
                # print(json)
        else:
            start_time = time.time()
            async with session.post(url, json=data, headers=headers) as resp:
                # json = await resp.json()
                text = await resp.read()
                print("text：", text)
        return text
                # print(json)


# 登陆
async def login(usernames):
    # res_texts = []
    tasks = []
    pattern = r'"token":"(.*?)"'
    token_compile = re.compile(pattern)
    url = 'https://test2.data4truth.com/student/login/login'
    print("url:", url)
    method = 'POST'
    for username in usernames:
        data = {"phoneNumber": username, "password": "123456"}
        tasks.append(asyncio.create_task(fetch(method, url, data=data)))
    return await asyncio.wait(tasks)
        # try:
        #     res_text = await fetch(method='POST', url=url, data=data)
        #     token = base.re_findall(token_compile, res_text)
        #     print(username, ':', token)
        #     if token == []:
        #         raise Exception("Get token failed!")
        #     else:
        #         print(token[0])
        #         return token[0]
        # except Exception as e:
        #
        #     raise e


# 获取练习题列表
async def get_exercise(headers):
    request_data = get_request_datas()["getExercise"]
    method = request_data["method"]
    url = request_data["url"]
    print("url:", url)
    data = request_data["data"]
    user_num = len(headers)
    tasks = []
    for asyn_num in range(1, user_num+1):
        # print("url_%s" % asyn_num, url)
        tasks.append(asyncio.create_task(fetch(method, url, data=data, headers=headers[asyn_num - 1])))
    await asyncio.wait(tasks)


# 获取练习题题目
async def get_question(headers):
    request_data = get_request_datas()["getQuestion"]
    method = request_data["method"]
    url = request_data["url"]
    print("url:", url)
    user_num = len(headers)
    tasks = []
    for i in range(1, user_num+1):
        exercise_id = "155%08d-1" % i
        request_data = get_request_datas(exercise_id=exercise_id)["getQuestion"]
        data = request_data["data"]
#        print("url_%s" % i, url)
        tasks.append(asyncio.create_task(fetch(method, url, data=data, headers=headers[i - 1])))
    await asyncio.wait(tasks)


# 做练习题,提交一道题目做题结果
async def submit_exercise(headers, question_id):
    start_time = base.local_time()
    time.sleep(1)
    end_time = base.local_time()
    request_data = get_request_datas(question_id=question_id)["getExercise"]
    method = request_data["method"]
    url = request_data["url"]
    print("url:", url)
    user_num = len(headers)
    tasks = []
    for i in range(1, user_num + 1):
        exercise_id = "155%08d-1" % i
        request_data = get_request_datas(exercise_id=exercise_id, question_id=question_id,
                                         start_time=start_time, end_time=end_time)["getExercise"]
        data = request_data["data"]
        # print("url_%s" % i, url)
        tasks.append(asyncio.create_task(fetch(method, url, data=data, headers=headers[i - 1])))
    await asyncio.wait(tasks)


# 获取练习题做题结果
async def log_out(headers):
    request_data = get_request_datas()["logout"]
    method = request_data["method"]
    url = request_data["url"]
    print("url:", url)
    user_num = len(headers)
    tasks = []
    for i in range(1, user_num + 1):
        tasks.append(asyncio.create_task(fetch(method, url, headers=headers[i - 1])))
    await asyncio.wait(tasks)


# 运行测试脚本
def run_test(user_num):
    print("Performance testing ......")
    users_headers = get_users_headers()
#    run_submit_exercise(users_headers)
    asyncio.run(get_exercise(users_headers))
    # asyncio.run(log_out(users_headers))
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(get_exercise(users_headers))
#     loop.run_until_complete(get_question(users_headers))
   # question_id_list = ['0101010003001004', '0101010003001014', '0101010003001020',
   #                     '0101010003001021', '0101010003001025', '0101010003001059',
   #                     '0101010003001050', '0101010003001046',
   #                     '0101010005001009', '0101010005001011']
   # for question_id in question_id_list:
   #     loop.run_until_complete(submit_exercise(users_headers, question_id))
   # get_question(users_headers)


def count_elapsed(file_name):
    print("Counting for average elapse ......")
    elapsed_pattern = "elapsed:(.*)"

    # 统计整体平均请求时间
    with open(file_name) as fp:
        text = fp.read()
    elapsed_results = base.re_findall(elapsed_pattern, text)
    elapsed_sum = 0
    for elapsed in elapsed_results:
        elapsed_sum += float(elapsed)
    avg_elapse = elapsed_sum/len(elapsed_results)
    # print(elapsed_sum)
    print("The average elapse is: ", avg_elapse)

    # 按url统计平均请求时间
    pass

    local_time = base.local_time()
    local_date = base.local_date()
    with open('data/elapsed-%s.txt' % local_date, 'a+') as fp:
        fp.write(local_time+' '+str(avg_elapse)+'\n')


if __name__ == '__main__':
    # usernames = ('15500000001', '15500000002')
    # res_texts = asyncio.run(login(usernames))
    # print(res_texts)
    run_test(2)



