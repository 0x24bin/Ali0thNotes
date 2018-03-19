# -*- coding:utf8 -*-
# python2


import requests
import re
import os
import sys
import time
import shutil
from settings import *
from base import find_regex


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def write_log(content, showtime=False):
    """
    对log文件的规则读取
    :param content: 文件文本内容
    :type content: str
    :param showtime: 是否显示时间
    :type showtime: bool
    :return： 匹配到的规则列表
    :rtype: list
    """
    if showtime:
        content = ("{0} {1}").format(content, format(get_time()))
    else:
        content = ("{0}").format(content)
    print content
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    with open(LOG_PATH + "log", "a") as f:
        f.write(content + "\n")


def rename_log(file_name, endwith=".log"):
        # rename log
        shutil.copyfile(LOG_PATH + "log", LOG_PATH + file_name + endwith)
        os.remove(LOG_PATH + "log")


def read_log(content, method):
    """
    对log文件的规则读取
    :param content: 文件文本内容
    :type content: str
    :param method: 
            o:    read official rule
            a:    read add rule
            oa:   read both
            i:    read ignore rules
    :type method: str    
    :return： 匹配到的规则列表
    :rtype: list
    """
    if method == "o":
        regex = r'official : (.*)'
        match = find_regex(content, regex)
        return match
    elif method == "a":
        regex = r'add : (.*)'
        match = find_regex(content, regex)
        return match
    elif method == "oa":
        regex = r'official : (.*)\n|add : (.*)\n'
        match = find_regex(content, regex)
        match_list = []
        for arg_tuple in match:
            if arg_tuple[0] == "":
                arg_tuple_str = match_list.append(arg_tuple[1])
            else:
                arg_tuple_str = match_list.append(arg_tuple[0])
        return match_list
    elif method == "i":
        regex = r'\n[ ]?: ((?:alert|drop|log|pass|reject|sdrop|activate|dynamic)\s.+;\s*\))'
        match = find_regex(content, regex)
        return match
