#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/9 11:15
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : batch_modify_file_name.py
import os


def batch_modify_file_name(path):
    """
    批量修改文件夹目录下文件名
    :param path: path_to_folder 结尾带'/'
    :return: 默认将文件名修改成 file1、file2、file3...
    """
    f = os.listdir(path)  # 获取该目录下所有文件，存入列表中

    for i in range(len(f)):
        suffix = "." + f[i].split(".")[-1]  # 获取原文件名后缀
        old_name = path + f[i]  # 设置旧文件名（就是路径+文件名）
        new_name = path + "file" + str(i + 1) + suffix  # 设置新文件名
        os.rename(old_name, new_name)  # 用os模块中的rename方法对文件改名
        print(old_name, "======>", new_name)


if __name__ == "__main__":
    folder_path = ""
    batch_modify_file_name(folder_path)
