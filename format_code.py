#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/7 22:08
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : format_code.py
import os

from config import PATH


def format_py_code(path_or_file):
    """
    格式化 python 代码，可以接收文件夹路径、文件路径、当前路径下的目录名
    :param path_or_file: path_to_python_project or path_to_python_file
    """
    if os.path.isdir(path_or_file):
        g = os.walk(path_or_file)
        for path, dir_list, file_list in g:
            for file_name in file_list:
                if file_name.endswith('.py'):
                    file_path = os.path.join(path, file_name)
                    os.system('autopep8 --in-place --aggressive --aggressive {}'.format(file_path))
                    print(file_name + '---------------------- ok...')
    elif os.path.isfile(path_or_file):
        os.system('autopep8 --in-place --aggressive --aggressive {}'.format(path_or_file))
        print(path_or_file + '---------------------- ok...')
    else:
        print("it's a special file(socket,FIFO,device file)")


if __name__ == '__main__':
    my_path = PATH
    format_py_code(my_path)
