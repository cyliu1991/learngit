# coding=utf-8
import pymysql
import time

def create_conn():
    host = "183.131.202.146"
    user = "education"
    password = "education"
    db = "testeducation"
    conn = pymysql.connect(host=host, user=user, password=password, db=db)
    return conn


def clear_database(conn):
    for table in ['`teacher_question`', '`testpaper_question`', '`student_testpaper_question`']:
        with conn.cursor() as cursor:
            try:
                sql = "SELECT * FROM %s WHERE testpaper_id like '%%1111%%'" % table
                print(sql)
                cursor.execute(sql)
                res = cursor.fetchall()
                print(type(res))
                print(res)
                if res:
                    sql = "DELETE  FROM %s WHERE testpaper_id like '%%1111%%'" % table
                    cursor.execute(sql)
            except Exception as e:
                conn.rollback()
                raise e
    conn.commit()


def create_done_exercise_list(conn):
    clear_database(conn)
    # print(db)
    sql1 = "INSERT INTO `testeducation`.`teacher_question`" \
          "(`testpaper_id`, `class_id`, `teacher_id`, `student_id`, `testpaper_type`, `testpaper_name`, `create_time`, " \
          "`creater_id`, `item_id`, `save_flag`, `source_paper_id`, `id`) " \
          "VALUES ('1111-1111-1111-1111-%s', NULL, '010101001001', '0101010011404023', 1," \
          " '陈翰韬强化训练-1111-1111-%s', '%s', '010102001001', NULL, 1, '0101020016001'," \
          "'1111-1111-1111-1111-%s')"

    sql2 = "INSERT INTO `testeducation`.`testpaper_question`(`testpaper_id`, `question_id`, `point_id`, `rate`) " \
           "VALUES ('1111-1111-1111-1111-%s', '0101020015001021', 'Ae01', 0.35135135135135137)"
    sql3 = "INSERT INTO `testeducation`.`student_testpaper_question`" \
           "(`student_id`, `testpaper_id`, `question_id`, `student_question_subtract`, `student_question_score`," \
           " `student_question_score_rate`, `student_question_answer`, `student_question_corret`," \
           " `student_question_answer_point`, `student_question_point_correct`) " \
           "VALUES ('0101010011404023', '1111-1111-1111-1111-%s'," \
           " '0101020015001021', NULL, NULL, NULL, 'test', 0, NULL, NULL)  "

    create_time = time.strftime("%Y-%m-%d %X", time.localtime())
    for i in range(10):
        print(i)
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql1 % (i, i, create_time, i))
                cursor.execute(sql2 % i)
                cursor.execute(sql3 % i)
            conn.commit()
        except Exception as e:
            print(e)


def remove_conn(conn):
    conn.close()


def setup():
    print("Preparing for testting...")
    conn = create_conn()
    create_done_exercise_list(conn)
    remove_conn(conn)


def teardown():
    print("Cleaning...")
    conn = create_conn()
    clear_database(conn)
    remove_conn(conn)


def compare_result(list1, list2):
    flag = 1
    for a in list1:
        if a in list2:
            flag = 0
            break
    return flag


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


def count_finished_testpaper(student_id):
    sql = "SELECT testpaper_id FROM `teacher_question` WHERE student_id='%s' % student_id"
    conn = create_conn()
    with conn.cursor() as cursor:
        cursor.execute(sql)
        res = cursor.fetchall()
#        print(res)
    testpaper_count = 0
    for testpaper_id in res:
        finished_flag = judge_finished_testpaper(conn, testpaper_id[0], student_id)
        if finished_flag:
            print(testpaper_id[0])
            testpaper_count = testpaper_count + 1
    conn.close()
    return testpaper_count




if __name__ == "__main__":
#    testpaper_id = '010102001001-11303033-20190117-145315-21'
    student_id = '0101010011404023'
#    judge_finished_testpaper(testpaper_id, student_id)
    res = count_finished_testpaper(student_id)
    print(res)