#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/10 13:55
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : save_csv_to_mysql.py


# 导入必要模块
import pandas as pd
from sqlalchemy import create_engine

from secure import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)  # 初始化数据库连接，使用pymysql模块

df = pd.read_csv("E://mpg.csv", sep=',')  # 读取本地CSV文件

df.to_sql('mpg', engine, index=False)  # 将新建的DataFrame储存为MySQL中的数据表，不储存index列

print("Write to MySQL successfully!")
