#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/9 18:58
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : format_python_code_asyncio.py
import os
import time
from concurrent import futures
from multiprocessing.dummy import Pool

from config import PATH


def format_single_file(p):
    os.system('autopep8 --in-place --aggressive --aggressive {}'.format(p))
    name = p.split('/')[-1]
    print(name + '-' * (40 - len(name)) + 'ok...')


def format_py_code(path_or_file):
    """
    格式化 python 代码，可以接收文件夹路径、文件路径、当前路径下的目录名
    :param path_or_file: path_to_python_project or path_to_python_file
    """
    if os.path.isdir(path_or_file):
        task_list = []
        g = os.walk(path_or_file)
        for path, dir_list, file_list in g:
            for file_name in file_list:
                if file_name.endswith('.py'):
                    file_path = os.path.join(path, file_name)
                    task_list.append(file_path)
        print(len(task_list))
        # executor = futures.ThreadPoolExecutor(500)
        # executor.map(format_single_file, task_list)
        pool = Pool(8)
        pool.map(format_single_file, task_list)

    elif os.path.isfile(path_or_file):
        format_single_file(path_or_file)
    else:
        print("it's a special file(socket,FIFO,device file)")


if __name__ == '__main__':
    my_path = PATH
    t0 = time.time()
    format_py_code(my_path)
    time_consuming = time.time() - t0
    print('消耗时间: ', time_consuming)
