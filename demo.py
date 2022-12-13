#####TODO:format usage
# print("{:*^100s}".format("start"))

#####TODO:time usage
# import time
# time_stamp = time.localtime()
# report_name = (("{:0>2}" * 3 + '-' + "{:0>2}" * 3)
#                .format(time_stamp.tm_year % 2000,
#                        time_stamp.tm_mon,
#                        time_stamp.tm_mday,
#                        time_stamp.tm_hour,
#                        time_stamp.tm_min,
#                        time_stamp.tm_sec))
# report_name = ("BenchTestData_Report_{}.csv".format(report_name))
# print(report_name)
# current_time = time.time()
# print(time.ctime(current_time))
# print(type(time.ctime(current_time)))

#####TODO:Path usage
# from pathlib import *
# temp = Path.cwd().joinpath("file.csv")
# print(temp)
# temp1 = Path(temp)
# print(temp1)
# temp3 = Path.cwd().joinpath('a','b')
# try:
#     temp3.mkdir(parents=True, exist_ok=False)
# except FileExistsError:
#     print("MSG: file exists")
# else:
#     print("MSG: file not exist")
# finally:
#     print("MSG: finally does")
#
# temp4 = './c/d/../e'
# print(Path(temp4).resolve())
# dir = str(temp.parent)
# print(dir)
# print(type(dir))
# print(temp.parent.name)

#####TODO:List usage
# head_line = [
#     "LOG_DIR",
#     "LOG_NAME",
#     "LOG_SUFFIX",
#     "LOG_SIZE",
#     "LOG_CTIME",
# ]
# print(head_line)
# print(','.join(head_line))
# print(len(head_line))
# head_line.append('')
# head_line.append('')
# print(','.join(head_line))

#####TODO:range usage
# for i in range(10):
#     print (i)

#####TODO:If and for loop performance
# import time
#
# start_time = time.time()
# start_cpu_time = time.perf_counter()
#
# x = 'a'
#
# if 'a' == x:
#     for i in range(1000000):
#         print('.', end='')
#
# # for i in range(1000000):
# #     if 'a' == x:
# #         print('.', end='')
#
# end_time = time.time()
# end_cpu_time = time.perf_counter()
# print("\nMSG: used time is {:.6f} s.".format(end_time - start_time))
# print("MSG: CPU used time is {:.6f} s.".format(end_cpu_time - start_cpu_time))

#####TODO:Operator usage
# i = 10
# while i > 0:
#     i-=1
#     print(i)
#
# print(2**20)

#####TODO:String usage
# a = 'hello'
# x = a.find('a')
# print (x)

#####TODO:line.find vs regex performance
# import time
# from re import *
#
# demo_str = 'x' * 10 + 'y' + 'z' * 10
# match_times = 10000000
#
# start_time = time.time()
#
# find_index = -1
# for i in range(match_times):
#     find_index = demo_str.find('y')
# if find_index > 0:
#     print("\nindex is {}".format(find_index))
#
# end_time = time.time()
# print("MSG: line.find used time is {:.6f} s.".format(end_time - start_time))
#
# start_time = time.time()
#
# find_index_r = ''
# for i in range(match_times):
#     find_index_r = match(r'^\w+y', demo_str)
# if find_index_r:
#     print("index is {}".format(find_index_r))
#
# end_time = time.time()
# print("MSG: regex match used time is {:.6f} s.".format(end_time - start_time))
#
# start_time = time.time()
#
# find_index_r = ''
# for i in range(match_times):
#     find_index_r = search(r'y', demo_str)
# if find_index_r:
#     print("index is {}".format(find_index_r))
#
# end_time = time.time()
# print("MSG: regex match used time is {:.6f} s.".format(end_time - start_time))

#####TODO:Regex usage
# from re import *
#
# demo_str = "val:0xffc5c"
# reg = search(r'val:0x(\w+)', demo_str)
# print(reg.group(1))
# str2 = ("{:0>6s}".format(reg.group(1)))
# print(str2)
# a = str2[0]
# b = str2[1:]
# print(a)
# print(b)

#####TODO:Hex Dec change
# hex_number = 'ff'
# print(int(hex_number, 16))
# dec_number = 255
# print(hex(dec_number))
# div_number = 255 / 2
# print(div_number)

# #####TODO:range usage
# for i in range(10,0,-1):
#     print(i)
# with open("./README.md", 'r') as f:
#     lines = f.readlines()
# print("line count is {}".format(len(lines)))

# #####TODO:tuple usage
# demo_list = [1,3,5,7]
# demo_tuple = tuple(demo_list)
# tuple_len = len(demo_tuple)
# print(demo_tuple)
# print(tuple_len)

# #####TODO:zip usage
# a = "A,B,C,1,,\n"
# b = "a,b,c,None,2,\n"
# print(a.rstrip(',\n'))
# print(b.rstrip(',\n'))
# a = [str(x) for x in a.rstrip(',\n').split(',')]
# b = [str(x) for x in b.rstrip(',\n').split(',')]
# demo_list = ['-'.join(x) for x in zip(a, b)]
# print(demo_list)
# with open("./README.md", 'r') as f:
#     lines = f.readlines()
# for line in lines:
#     print(line)
#     item_list = [str(x) for x in line.split(' ')]
#     print(item_list)

# #####TODO:index usage
# demo_list = [1,5,1,2,1,0,1,7,1,9,8]
# find_num = 8
# try:
#     index = demo_list.index(find_num)
# except ValueError as e:
#     print("WARN: {}".format(e))
# else:
#     print("index of {} is {}".format(find_num, index))

# #####TODO:dict usage
# demo_dict = {
#     '' : 1e+15,
#     'a' : 2,
#     1 : 3,
# }
# demo = ""
# print(demo_dict[demo])

# #####TODO:unicodedata usage
# import unicodedata
#
# print(unicodedata.numeric('-2.0'))

# #####TODO:float usage
# demo_digit = '-1e+3'
# print(float(demo_digit) + 1)

# #####TODO:strip usage
# demo_str = 'mV'
# unit = demo_str.rstrip('V')
# print(unit)

# #####TODO:list usage
# unit_type = [
#     'V',  # voltage
#     'A',  # current
#     'W',  # power
#     'S',  # time
#     'F',  # capacitance
#     'HZ',  # frequency
#     'R', 'OHM',  # resistance
#     'LSB',  # Least Significant Bit
#     'DB',  # DeciBel
#     'DBM',  # DeciBel per Milli watt
# ]
#
# print ('V' in unit_type)
#
# demo_str = 'kHZ'
# print('hz'.upper() in demo_str)

# #####TODO:re usage
# import re
# unit_type_list = [
#     'V',  # voltage
#     'A',  # current
#     'W',  # power
#     'S',  # time
#     'F',  # capacitance
#     'HZ',  # frequency
#     'R', 'OHM',  # resistance
#     'LSB',  # Least Significant Bit
#     'DB',  # DeciBel
#     'DBM',  # DeciBel per Milli watt
# ]
#
# demo_str = 'Hz'
# for t in unit_type_list:
#     if t in demo_str.upper():
#         print("{} is found in {}".format(t, demo_str))
#         print(r'^(\w)?{}$'.format(t))
#         match = re.match(r'^(\w)?{}$'.format(t), demo_str, re.IGNORECASE)
#         print(type(match))
#         if not match is None:
#             print(match.group(0))
#             print(match.group(1))
#         else:
#             print("match is {}".format(match))
#
# def unit_split(unit_type_list, unit):
#     """
#     Split the unit into unit factor and unit type.
#     """
#     unit_factor = ""
#     unit_type = ""
#     for t in unit_type_list:
#         if t in unit.upper():
#             unit_type = t
#             matched = re.match(r'^(\w)?{}$'.format(t), unit, re.IGNORECASE)
#             if matched is None:
#                 print("WARN: unit factor matched failed in '{}' !!".format(unit))
#                 return None
#             else:
#                 if not matched.group(1) is None:
#                     unit_factor = matched.group(1)
#
#     return unit_factor, unit_type
#
# demo_get = unit_split(unit_type_list, demo_str)
# print(demo_get)

# #####TODO:dict usage
# factor_dict = {
#     'M': 1e+6,
#     'K': 1e+3,
#     'k': 1e+3,
#     '': 1,
#     'm': 1e-3,
#     'u': 1e-6,
#     'n': 1e-9,
#     'p': 1e-12,
#     'f': 1e-15,
# }
#
# demo_factor = 'a'
#
# if demo_factor in factor_dict:
#     print("in")
# else:
#     print("not in")

# #####TODO: incorrect unused local variable warning feedback
data = '0.1'
float_data = 0
try:
    float_data = float(data)
except ValueError:
    print("WARN: the data '{}' not a digit !!".format(data))
else:
    print(float_data)

