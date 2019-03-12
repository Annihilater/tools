#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/2 00:21
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : write_to_excel.py
import os

import xlwt
from xlrd import open_workbook
from xlutils.copy import copy as workbook_copy


def set_style(name, height, bold=False):  # 设置表格样式
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


def write_to_excel(title_list, file_path, data):
    """
    写入 excel
    :param title_list:[title1, title2, title3, title4, ...]
    :param file_path: 'path_to_excel'
    :param data: [[1,2,3, ...], [1, 2, 3, ...], [1, 2, 3, ...], ...]
    """
    if not os.path.exists(file_path):
        book = xlwt.Workbook()
        file_name = file_path.split("/")[-1]
        sheet1 = book.add_sheet(sheetname=file_name, cell_overwrite_ok=True)
        for i in range(0, len(title_list)):
            sheet1.write(0, i, title_list[i], set_style("Times New Roman", 220, True))
        book.save(file_path)

    read_book = open_workbook(file_path, on_demand=True)  # 用wlrd提供的方法读取一个excel文件
    base_rows = read_book.sheets()[0].nrows  # 用wlrd提供的方法读取一个excel文件
    write_book = workbook_copy(read_book)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    sheet1 = write_book.get_sheet(0)  # xlwt 对象的 sheet1 具有 write 权限方便后面写入数据
    for row in range(0, len(data)):
        for column in range(0, len(data[row])):
            sheet1.write(
                base_rows + row,
                column,
                data[row][column],
                set_style("Times New Roman", 220, True),
            )
    write_book.save(file_path)

    print("成功写入 excel")
