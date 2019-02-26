#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/2/26 18:59
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : get_video_files_sum_time.py
import cv2
import os
import re

from config import video_path1 as video_path


def get_videos_duration(video_folder_path):
    print(video_folder_path)
    k = get_files(video_folder_path)
    data = []
    for name in k:
        chapter = re.findall('(\d*)-', name)[0]
        part = re.findall('-(\d*)', name)[0]
        data.append([int(chapter), int(part), name])

    data = sorted(data)
    sum_time = 0
    for d in data:
        name = d[2]
        file_path = video_path + '/' + name
        time = get_video_duration(file_path)
        sum_time += time  # 单位是秒
        # print(name, time)

    print('秒数', sum_time)
    print('分钟', turn_to_minutes(sum_time))
    print('小时', turn_to_hours(sum_time))


def get_files(video_folder_path):
    g = list(os.walk(video_folder_path))[0][2]
    k = sorted(g)
    k.remove('.DS_Store')
    k.remove('课程目录.txt')
    print('获取视频文件 ok')
    return k


def get_video_duration(path):  # 获取单个视频文件的时长
    cap = cv2.VideoCapture(path)  # path是视频文件的绝对路径，防止路径中含有中文时报错，需要解码
    if cap.isOpened():  # 当成功打开视频时cap.isOpened()返回True,否则返回False
        # get方法参数按顺序对应下表（从0开始编号)
        rate = cap.get(5)  # 帧速率
        frame_number = cap.get(7)  # 视频文件的帧数
        duration = int(frame_number / rate)  # 帧速率/视频总帧数 是时间， int 是用来取整
        return duration
    else:
        return '视频文件打开失败'


def turn_to_minutes(seconds):
    minutes = int(seconds / 60)
    return minutes


def turn_to_hours(seconds):
    hours = int(seconds / 3600)
    remainder = int((seconds / 60) % 60)  # 取余数分钟
    result = str(hours) + ' hours ' + str(remainder) + ' minutes'
    return result


if __name__ == '__main__':
    get_videos_duration(video_path)
