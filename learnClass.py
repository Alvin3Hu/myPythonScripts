#####TODO:class dict
# class Person:
#     """for learning the class from python"""
#
#     age = 3
#     height = 170
#
#     def __init__(self, name, age=18):
#         self.name = name
#         self.age = age
#
#
# tom = Person('Tom')
# jerry = Person('Jerry', 20)
#
# Person.age = 30
# print(Person.age, tom.age, jerry.age)
# print(Person.height, tom.height, jerry.height)
# print(jerry.__dict__)
# print(tom.__dict__)
#
# jerry.height = 175
# print(Person.height, tom.height, jerry.height)
# print(jerry.__dict__)
# print(tom.__dict__)
#
# tom.height += 10
# print(Person.height, tom.height, jerry.height)
# print(jerry.__dict__)
# print(tom.__dict__)
#
# Person.weight = 70
# print(Person.weight, tom.weight, jerry.weight)
# print(jerry.__dict__)
# print(tom.__dict__)
# print(type(tom).__dict__)
# print(tom.__class__.__dict__['weight'])
# print(tom.weight)
#####class dict

#####TODO:class method calling
# class Person:
#     def method(self):
#         print("{}'s method".format(self))
#
#     @classmethod
#     def class_method(cls):
#         print('class = {0.__name__}({0})'.format(cls))
#         cls.HEIGHT = 170
#
#     @staticmethod
#     def static_method():
#         print(Person.HEIGHT)
#
#
# # print(Person.method())
# print(Person.class_method())
# print(Person.static_method())
# print(Person.__dict__)
#
# tom = Person()
# print(tom.method())
# print(tom.class_method())
# print(tom.static_method())
# print(tom.__dict__)
# print(tom.HEIGHT)
#
#####class method calling

#####TODO:private and protect
# class Person:
#     def __init__(self, name, age=10):
#         self.name = name
#         self.__age = age
#
#     def growUp(self, i=1):
#         if i > 0 and i < 100:
#             self.__age += i
#
#     def showAge(self):
#         return self.__age
#
#
# p1 = Person('Tom')
# print(p1.__dict__)
#
# p1.growUp(55)
# print(p1.__dict__)
# print(p1._Person__age)
# print(p1.showAge())
# p1.__age = 100
# print(p1.showAge())
# print(p1.__age)
# print(p1.__dict__)
#
#####private and protect

#####TODO:property decorator
# class Person:
#     def __init__(self, name, age=18):
#         self.name = name
#         self.__age = age
#
#     @property
#     def age(self):
#         print('getter')
#         return self.__age
#
#     @age.setter
#     def age(self, age):
#         print('setter')
#         self.__age = age
#
#     @age.deleter
#     def age(self):
#         print('deleter')
#         del self.__age
#
#
# tom = Person('Tom')
# print(tom.age)
# tom.age = 22
# print(tom.age)
# print(tom.__dict__)
# del tom.age
# print(tom.__dict__)
# print(type(tom).__dict__)
#####property decorator

#####TODO:property function
# class Person:
#     def __init__(self, name, age=18):
#         self.name = name
#         self.__age = age
#
#     def getage(self):
#         print('getter')
#         return self.__age
#
#     def setage(self, age):
#         print('setter')
#         self.__age = age
#
#     def delage(self):
#         print('deleter')
#         del self.__age
#
#     age = property(getage, setage, delage, 'age property')
#
#
# tom = Person('Tom')
# print(tom.age)
# tom.age = 22
# print(tom.age)
# print(tom.__dict__)
# del tom.age
# print(tom.__dict__)
# print(type(tom).__dict__)
#####property function

#####TODO:object destroy
import time


class Person:
    def __init__(self, name, age=18):
        self.name = name
        self.__age = age

    def __del__(self):
        print('delete {}'.format(self.name))


tom = Person('tom')
tom.__del__()
tom.__del__()
tom.name
tom2 = tom
tom3 = tom2
print(tom, tom2, tom3)
del tom
time.sleep(3)
del tom2
print('='*33)
del tom3


#####object destroy
