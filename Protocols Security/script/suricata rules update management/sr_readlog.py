# -*- coding:utf8 -*-
# python2
"""
Suricata Rules Read Log

SR_ReadLog is short for Suricata Rules Read Log.

Author : ali0th
Date   : 18/3/9
Email  : martin2877 at foxmail.com
"""

import requests
import re
import os
import sys
import time


LOCAL_PATH = r"C:/Users/muhe/Desktop/links/tophant/suricata/nazgul-ids_prs2.1/rules/" # local rules path
TEMP_PATH = r"C:/Users/muhe/Desktop/links/wirte/Ali0thNotes/Protocols Security/script/suricata rules update management/sr_compare_log/" # temp addr for file cache
LOG_PATH = TEMP_PATH
LOG_METHOD = "w"
TEMP_FILE = ""


def print2(content):
    print content

def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_text(path, method):
    """
    three methods to get text
    1. open local file
    2. requests url
    3. read temp file first else download url
    """
    try:
        if method == 1:
            if os.path.exists(path):
                with open(path,"r") as f:
                    return f.read(), True
            else:
                return [], False
        elif method == 2:
            r = requests.get(path, stream=True)
            return r.text, True
        elif method == 3: 
            temp_file_name = os.path.basename(path)
            if not os.path.exists(TEMP_PATH):
                os.mkdir(TEMP_PATH)
            temp_file = TEMP_PATH + temp_file_name
            if os.path.exists(temp_file):
                write_log("file exist, opening : {0}".format(temp_file) )
                return get_text(temp_file, 1)
            else:
                write_log("downloading : {0}".format(path) )
                file_text, is_text = get_text(path, 2)
                with open(temp_file, "w") as f:
                    f.write(file_text)
                return file_text, True

    except Exception as e:
        return e, False


def find_regex(content, regex):
    pattern = re.compile(regex,re.I)
    match = pattern.findall(str(content))
    return match


def get_files(path, rules):
    all_files = []
    for fpath, dirname, fnames in os.walk(path):   # os.walk是获取所有的目录
        for filename in fnames:
            path_name = os.path.join(fpath,filename)
            for value in rules:
                if path_name.endswith(value): # 判断是否是"xxx"结尾
                    all_files.append(path_name)
    return all_files


def read_log(content, method):
    """
    method:
    1. read official rule
    2. read add rule
    3. read both
    4. read ignore rules
    """
    if method == 1:
        regex = r'official : (.*)'
        match = find_regex(content, regex)
        return match
    elif method == 2:
        regex = r'add : (.*)'
        match = find_regex(content, regex)
        return match
    elif method == 3:
        regex = r'official : (.*)\n|add : (.*)\n'
        match = find_regex(content, regex)
        match_list = []
        for arg_tuple in match:
            if arg_tuple[0] == "":
                arg_tuple_str = match_list.append(arg_tuple[1])
            else:
                arg_tuple_str = match_list.append(arg_tuple[0])
        return match_list
    elif method == 4:
        regex = r'\n[ ]?: ((?:alert|drop|log|pass|reject|sdrop|activate|dynamic)\s.+;\s*\))'
        match = find_regex(content, regex)
        return match



def name(log_path):
    """
    从log文件里获取不需要更新的sid和新增的sid
    :param log_path: 文件路径
    :type log_path: str
    :return： 不需要被更新的规则的 sid 列表 和 新增规则的 sid 列表
    :rtype: list, list
    """
    # 不需要被更新的规则的 sid
    no_update_list = []
    # 新增规则的 sid
    new_add_list = []

    def get_sid(content):
        regex = r"sid: ?([0-9]*?);"
        sid = find_regex(content, regex)
        if len(sid)>=1:
            return sid[0]
        else:
            return sid

    all_files = get_files(log_path, ["log"])
    for file_path in all_files:
        content, is_text = get_text(file_path, 1)
        if is_text:
            no_update_list_single_file = read_log(content, 4)
            new_add_list_single_file = read_log(content, 2)
            if no_update_list_single_file:
                for value in no_update_list_single_file:
                    sid = get_sid(value)
                    no_update_list.append(sid)
            if new_add_list_single_file:
                for value in new_add_list_single_file:
                    sid = get_sid(value)
                    new_add_list.append(sid)
    return no_update_list, new_add_list


if __name__ == '__main__':
    list1, list2 = name("C:/Users/muhe/Desktop/test/")
    print2(list1)
    print2(len(list1))
    print2(list2)
    print2(len(list2))