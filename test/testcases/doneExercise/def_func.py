# !/usr/local/bin/python3
import time
import pymysql
from operator import itemgetter


def create_done_exercise_list(conn, student_id):
    clear_database(conn)
    # print(db)
#    question_id = '0101010003001014'
    sql1 = "INSERT INTO `teacher_question`" \
          "(`testpaper_id`, `class_id`, `teacher_id`, `student_id`, `testpaper_type`, `testpaper_name`, `create_time`, " \
          "`creater_id`, `item_id`, `save_flag`, `source_paper_id`, `id`) " \
          "VALUES ('2222-1111-1111-1111-%s', NULL, '010102001001', '%s', 1," \
          " '测试-2222-1111-%s', '%s', '010102001001', NULL, 1, '0101020016001'," \
          "'2222-1111-1111-1111-%s')"

    sql2 = "INSERT INTO `testpaper_question`(`testpaper_id`, `question_id`, `point_id`, `rate`) " \
           "VALUES ('2222-1111-1111-1111-%s', '%s', 'Aa0101', 0.35135135135135137)"
    sql3 = "INSERT INTO `student_testpaper_question`" \
           "(`student_id`, `testpaper_id`, `question_id`, `student_question_subtract`, `student_question_score`," \
           " `student_question_score_rate`, `student_question_answer`, `student_question_corret`," \
           " `student_question_answer_point`, `student_question_point_correct`) " \
           "VALUES ('%s', '1111-1111-1111-1111-%s'," \
           " '%s', NULL, NULL, NULL, 'test', 0, NULL, NULL)  "
    sql4 = "INSERT INTO `question_action`(`student_id`, `testpaper_id`, `question_id`," \
           " `start_time`, `end_time`, `submit_action`, `action_result`, `action_data`) " \
           "VALUES ('%s', '1111-1111-1111-1111-%s', '%s', " \
           "'%s', '%s', 1, 0, 'test')"
    doneExerciseList = []
    for i in range(2):
        exercise_record = {}
        create_time = time.strftime("%Y-%m-%d %X", time.localtime())
        time.sleep(1)
        end_time = time.strftime("%Y-%m-%d %X", time.localtime())
#        print(i)
        exercise_record["exerciseName"] = ('测试-1111-1111-%s' % i)
        exercise_record["exerciseID"] = ('1111-1111-1111-1111-%s' % i)
        exercise_record["finishTime"] = end_time
        t = exercise_record
        doneExerciseList.append(t)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql1 % (i, student_id, i, create_time, i))
                for j in range(1, 3):
                    question_id = '010101000300100%s' % j
                    cursor.execute(sql2 % (i, question_id))
#                cursor.execute(sql3 % (student_id, i, question_id))
#                cursor.execute(sql4 % (student_id, i, question_id, create_time, end_time))
            conn.commit()
        except Exception as e:
            print(e)
    print(doneExerciseList)
    return doneExerciseList


def clear_database(conn):
    for table in ['`teacher_question`', '`testpaper_question`', '`student_testpaper_question`', '`question_action`']:
        with conn.cursor() as cursor:
            try:
                sql = "SELECT * FROM %s WHERE testpaper_id like '%%1111%%'" % table
#                print(sql)
                cursor.execute(sql)
                res = cursor.fetchall()
                if res:
                    sql = "DELETE  FROM %s WHERE testpaper_id like '%%1111%%'" % table
                    cursor.execute(sql)
            except Exception as e:
                conn.rollback()
                raise e
    conn.commit()


def setup(conn):
    print("Preparing for testting...")
    create_done_exercise_list(conn)


def teardown(conn):
    print("Cleaning...")
    clear_database(conn)


def judge_finished_testpaper(conn, testpaper_id, student_id ):
    sql1 = ("SELECT count(a.question_id) FROM `testpaper_question` a, question b" \
          " WHERE a.testpaper_id='%s' " \
          "AND a.question_id=b.question_id AND b.question_type_chinese IN" \
          " ('选择题', '填空题', '判断题', '计算题') and b.question_abnormal_reason is null" % testpaper_id)
#    print(sql1)
    sql2 = ("SELECT count(question_id) FROM `student_testpaper_question` " \
           "where testpaper_id='%s' and student_id='%s'" % (testpaper_id, student_id))
#    print(sql2)
    with conn.cursor() as cursor:
        cursor.execute(sql1)
        question_num = cursor.fetchone()
#        print(question_num)
        cursor.execute(sql2)
        question_finished_num = cursor.fetchone()
#        print(question_finished_num)
    if question_num == question_finished_num:
        finish_flag = 1
#        print("finished")
    else:
        finish_flag = 0
#        print("unfishished")
    return finish_flag


def get_finished_exercise(conn, student_id):
    sql = "SELECT testpaper_id, testpaper_name FROM `teacher_question` WHERE student_id='%s'" % student_id
#    print(sql)
    with conn.cursor() as cursor:
        cursor.execute(sql)
        res = cursor.fetchall()
#        print(res)
    testpaper_count = 0
    testpaper_ids = []
    for testpaper_id in res:
        finished_flag = judge_finished_testpaper(conn, testpaper_id[0], student_id)
        if finished_flag:
            testpaper_ids.append(testpaper_id[0])
    return testpaper_ids


# 返回作业列表最后一页的页数
def get_last_page(exercise_list, limit):
    doneExerciseNum = len(exercise_list)
    end_page = doneExerciseNum // limit + 1
    return end_page


# 返回已完成作业总数
def get_doneExercise_num(exercise_list):
    doneExerciseNum = len(exercise_list)
    return doneExerciseNum


# 升序返回作业列表
def get_doneExerciseList_timeIncrease(exercise_list, page, limit):
    start_page = (page - 1) * limit
    end_page = start_page + limit
    increase_list = sorted(exercise_list, key=itemgetter('finishTime'))[start_page:end_page]
    return increase_list


# 降序返回作业列表
def get_doneExerciseList_timeDecrease(exercise_list, page, limit):
    start_page = (page - 1) * limit
    end_page = start_page + limit
    increase_list = sorted(exercise_list, key=itemgetter('finishTime'), reverse=True)[start_page:end_page]
    return increase_list


if __name__ == "__main__":
    host = "183.131.202.146"
    user = "education"
    password = "education"
    db = "testeducation"
    conn = pymysql.connect(host=host, user=user, password=password, db=db)

#    testpaper_id = '010102001001-11303033-20190117-145315-21'
    student_id = '0101010011404023'
#    judge_finished_testpaper(testpaper_id, student_id)
    exercise_list = create_done_exercise_list(conn)
    print("exercise_list：", exercise_list)
    page_list = get_doneExerciseList_timeIncrease(exercise_list, 2, 6)
    print("page_list", page_list)
    print(len(page_list))
    clear_database(conn)
    conn.close()

