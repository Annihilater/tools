#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2020/4/21 5:29 下午
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : get_video_duration.py

import struct


def get_video_duration(video_file):
    with open(video_file, 'rb') as fp:
        data = fp.read()

    index = data.find(b'mvhd') + 4
    time_scale = struct.unpack('>I', data[index + 13:index + 13 + 4])
    durations = struct.unpack('>I', data[index + 13 + 4:index + 13 + 4 + 4])
    duration = durations[0] / time_scale[0]
    return duration


if __name__ == '__main__':
    t = get_video_duration('/Users/klause/Movies/我人生有两大选择，为的却都是同一件事道哥.mp4')
    print(t)
