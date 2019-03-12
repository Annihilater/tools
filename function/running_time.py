#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/2/28 19:36
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : running_time.py
import time


def running_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        used_time = end_time - start_time
        # 打印结果为 00:05:39 的形式
        print("运行时间: ", time.strftime("%H:%M:%S", time.gmtime(used_time)))

    return wrapper
