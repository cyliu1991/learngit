# coding=utf-8
from base import base as base
import time


def make_exercise(cursor, user_name, question_id_list, testpaper_id):
    sql_select_testpaper = "select testpaper_id from teacher_question where testpaper_id='%s'" % testpaper_id
    cursor.execute(sql_select_testpaper)
    fetch_testpaper = cursor.fetchone()
    # print("fetch_testpaper:", fetch_testpaper)

    if fetch_testpaper is None:
        sql_select_student_info = "SELECT student_id from student_info where user_name='%s'" % user_name

        cursor.execute(sql_select_student_info)
        fetch_student_info = cursor.fetchone()[0]
#        print(fetch_student_info)
        student_id = fetch_student_info
        create_time = time.strftime("%Y-%m-%d %X", time.localtime())
        sql_insert_testpaper = "INSERT INTO `teacher_question`" \
               "(`testpaper_id`, `class_id`, `teacher_id`, `student_id`, `testpaper_type`, `testpaper_name`, `create_time`, " \
               "`creater_id`, `item_id`, `save_flag`, `source_paper_id`, `id`) " \
               "VALUES ('%s', NULL, '010102001001', '%s', 1," \
               " '测试%s', '%s', '010102001001', NULL, 1, '0101020016001'," \
               "'%s')" % (testpaper_id, student_id, testpaper_id, create_time, testpaper_id)

        cursor.execute(sql_insert_testpaper)

        for question_id in question_id_list:
            sql_insert_testpaper_question = "INSERT INTO `testpaper_question`(`testpaper_id`, `question_id`, `point_id`, `rate`) " \
                   "VALUES ('%s', '%s', 'Aa0101', 0.35135135135135137)" % (testpaper_id, question_id)

            cursor.execute(sql_insert_testpaper_question)


if __name__ == '__main__':
    user = '17601007082'
    question_list1 = ['0101010003001004', '0101010003001014', '0101010003001020',
                      '0101010003001021', '0101010003001025']
    question_list2 = ['0101010003001059', '0101010003001050', '0101010003001046',
                      '0101010005001009', '0101010005001011']
    question_list3 = ['0101010003002020', '0101010006001018', '0101010011001036',
                      '0101010003001016', '0101010003001029']   # 带图
    question_list4 = ['0101010015003009', '0101010026001055', '0101010026002015',
                      '0101010032001057', '0101010032003013']
    question_lists = [question_list1, question_list2, question_list3, question_list4]
    question_list = ['0101010012002026']
    testpaper_id = '17601007082-test5'
    (server, conn) = base.create_conn()
    with conn.cursor() as local_cursor:
        try:
            make_exercise(local_cursor, user, question_list, testpaper_id)
        except Exception as e:
            conn.rollback()
            raise e
    conn.commit()
    conn.close()
    server.close()
