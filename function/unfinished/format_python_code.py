#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/7 22:08
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : format_python_code.py
import os
import time

from config import PATH


def format_single_file(p):
    os.system('autopep8 --in-place --aggressive --aggressive {}'.format(p))
    name = p.split('/')[-1]
    print(name + '-' * (40 - len(name)) + 'ok...')


def format_python_code(path_or_file):
    """
    格式化 python 代码，可以接收文件夹路径或者文件路径，或者当前路径下的目录名
    :param path_or_file: path_to_python_project or path_to_python_file
    """
    num = 0
    t0 = time.time()
    if os.path.isdir(path_or_file):
        g = os.walk(path_or_file)
        for path, dir_list, file_list in g:
            for file_name in file_list:
                if file_name.endswith('.py'):
                    file_path = os.path.join(path, file_name)
                    format_single_file(file_path)
                    num += 1
    elif os.path.isfile(path_or_file):
        format_single_file(path_or_file)
        num += 1
    else:
        print("it's a special file(socket,FIFO,device file)")

    time_consuming = time.time() - t0
    print('处理 ' + str(num) + ' 个文件; ' + '耗时: ' + str(time_consuming) + ' 秒')


if __name__ == '__main__':
    my_path = PATH
    format_python_code(my_path)
