import utils.make_exercise as make_exercise
from base import base

# 创建测试用户
def create_user(cursor, num):
    print("Creating users and exercise ......")
    password = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
    sql1 = "INSERT INTO `testeducation`.`student_info`(`student_id`, `user_name`, `password`, `picture_path`) " \
          "VALUES ('%s', '%s', '%s', NULL)"
    sql2 = "INSERT INTO `testeducation`.`student`(`student_id`, `student_name`, `student_gender`, `student_gender_chinese`, `student_birthday`, `student_grade`, `student_semester`, `student_unit`, `class_id`, `grade_id`, `school_id`, `textbook_id`, `student_graduate`) " \
           "VALUES ('%s', '%s', 1, '男', '2012-04-07', 1, '1.1', '1.1.08', '0101010011802', '01010100118', '010101001', 'A1', 0)"
    question_id_list = ['0101010003001004', '0101010003001014', '0101010003001020',
                        '0101010003001021', '0101010003001025', '0101010003001059',
                        '0101010003001050', '0101010003001046',
                        '0101010005001009', '0101010005001011']
    with open('../data/users.txt', 'a+') as fp:
        for i in range(1, num+1):
            student_id = "155%08d" % i
            user_name = "155%08d" % i
            fp.write(user_name + ',')
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

            cursor.execute(sql1 % (student_id, user_name, password))
            cursor.execute(sql2 % (student_id, user_name))
            make_exercise.make_exercise(cursor, user_name, question_id_list, testpaper_id)
    print("Creating users and exercise finished.")


if __name__ == '__main__':
    user_num = 15
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
