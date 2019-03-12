#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/10 14:20
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : xlsx_to_csv.py
import codecs
import csv

import pandas as pd
import xlrd


def xlsx_to_csv_pd():
    data_xls = pd.read_excel("../data/test.xlsx", index_col=0)
    data_xls.to_csv("../data/test.csv", encoding="utf-8")


def xlsx_to_csv():
    workbook = xlrd.open_workbook("../data/test.xlsx")
    table = workbook.sheet_by_index(0)
    with codecs.open("../data/test.csv", "w", encoding="utf-8") as f:
        write = csv.writer(f)
        for row_num in range(table.nrows):
            row_value = table.row_values(row_num)
            write.writerow(row_value)


if __name__ == "__main__":
    # xlsx_to_csv_pd()
    xlsx_to_csv()
