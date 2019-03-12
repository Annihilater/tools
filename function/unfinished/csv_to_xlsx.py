#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/10 14:14
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : csv_to_xlsx.py
import csv

import pandas as pd
import xlwt


def csv_to_xlsx_pd():
    csv = pd.read_csv("1.csv", encoding="utf-8")
    csv.to_excel("1.xlsx", sheet_name="data")


def csv_to_xlsx():
    with open("../data/test.csv", "r", encoding="utf-8") as f:
        read = csv.reader(f)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("data")  # 创建一个sheet表格
        l = 0
        for line in read:
            print(line)
            r = 0
            for i in line:
                print(i)
                sheet.write(l, r, i)  # 一个一个将单元格数据写入
                r = r + 1
            l = l + 1

        workbook.save("../data/test.xlsx")  # 保存Excel


if __name__ == "__main__":
    csv_to_xlsx_pd()
    csv_to_xlsx()
