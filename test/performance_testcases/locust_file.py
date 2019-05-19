from locust import Locust, TaskSet, task
from performance_testcases.StudentPerformanceTesting import run_test

class MyTaskSet(TaskSet):
    @task
    def my_task(self):
        run_test(500)

class MyLocust(Locust):
    task_set1 = MyTaskSet
    min_wait1 = 5000
    max_wait1 = 15000


