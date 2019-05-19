import time
import asyncio


def test1(user):
    print(user, '-test1:', time.strftime("%Y-%m-%d %X", time.localtime()))


def test2(user):
    print(user, '-test2:', time.strftime("%Y-%m-%d %X", time.localtime()))


async def runtest(user):
    test1(user)
    test2(user)



