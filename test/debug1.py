import time

def test1(i):
    print("user%s" % i, "test1", time.time())


def test2(i):
    print("user%s" % i, "test2", time.time())


def test(i):
    test1(i)
    time.sleep(1)
    test2(i)
    time.sleep(1)