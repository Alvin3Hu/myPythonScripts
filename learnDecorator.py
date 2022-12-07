"""Definition
装饰器本质上是一个Python函数(其实就是闭包)，它可以让其他函数在不需要做任何代码变动的前提下增加额外功能，装饰器的返回值也是一个函数对象。
装饰器用于有以下场景，比如:插入日志、性能测试、事务处理、缓存、权限校验等场景。

"""
#####TODO:decorator normal coding method
# import threading
# import time
#
#
# def how_much_time(func):
#     def inner():
#         t_start = time.time()
#         func()
#         t_end = time.time()
#         print("Total used {0}s time".format(t_end - t_start, ))
#
#     return inner
#
#
# def sleep_5s():
#     time.sleep(5)
#     print("%ds used" % (5,))
#
#
# def sleep_6s():
#     time.sleep(6)
#     print("%ds used" % (6,))
#
#
# sleep_5s = how_much_time(sleep_5s)
# sleep_6s = how_much_time(sleep_6s)
#
# t1 = threading.Thread(target=sleep_5s)
# t2 = threading.Thread(target=sleep_6s)
# t1.start()
# t2.start()
#####

#####TODO:decorator syntactic sugar coding style
import time
import threading


def how_much_time(func):
    def inner():
        t_start = time.time()
        func()
        t_end = time.time()
        print("Total used {0}s time".format(t_end - t_start, ))

    return inner


@how_much_time
def sleep_5s():
    time.sleep(5)
    print("%ds used" % (5, ))


@how_much_time
def sleep_6s():
    time.sleep(6)
    print("%ds used" % (6, ))


t1 = threading.Thread(target=sleep_5s)
t2 = threading.Thread(target=sleep_6s)
t1.start()
t2.start()

#####
