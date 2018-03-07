# -*- coding:utf8 -*-
"""
Suricata Rules Update Management

SRUM is short for Suricata Rules Update Management , a tool to compare and update rules between local and official.

Author : ali0th
Date   : 18/3/7
Email  : martin2877 at foxmail.com
"""

import requests
import re
import os
import sys
import time

OFFICIAL_PATH = r'https://rules.emergingthreats.net/open/suricata-4.0/rules/'
LOCAL_PATH = r"C:/Users/muhe/Desktop/links/tophant/suricata/nazgul-ids_prs2.1/rules/"

def get_text(path, method):
    try:
        if method == 1:
            with open(path, "r") as f:
                return f.read(), True
        elif method == 2:
            r = requests.get(path)
            return r.text, True
    except Exception as e:
        return e, False


def match_file(content):
    pattern = re.compile(r'<a href="[^?^/].*?">(.*?)</a>')
    match = pattern.findall(str(content))
    if match:
        print("Receive Offical Rules Success {0}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        return match,True
    else:
        return [],False


def get_files(path, rules):
    all_files = []
    for fpath, dirname, fnames in os.walk(path):   # os.walk是获取所有的目录
        for filename in fnames:
            path_name = os.path.join(fpath,filename)
            for value in rules:
                if path_name.endswith(value): # 判断是否是"xxx"结尾
                    all_files.append(path_name)
    return all_files


def find_regex(content, regex):
    pattern = re.compile(regex,re.I)
    match = pattern.findall(str(content))
    return match


def compare_files(file1, file2, regex=""):

    def compare_sid(content1, content2):
        re = r'sid:([0-9]*?);'
        sid_list1 = find_regex(content1, re)
        sid_list2 = find_regex(content2, re)
        for sid1 in sid_list1:
            if sid1 in sid_list2:
                re = r'.*sid:{0};.*'.format(sid1)
                print("="*20)
                print("local : {0}\n".format(find_regex(content1, re)[0]))
                print("official : {0}\n".format(find_regex(content2, re)[0]))
        for sid2 in sid_list2:
            if sid2 not in sid_list1:
                re = r'.*sid:{0};.*'.format(sid2)
                print("="*20)
                print("add : ", find_regex(content2, re)[0])

    if regex:
        re = r'.*{0}.*'.format(regex)
        result1 = find_regex(file1, re)
        result2 = find_regex(file2, re)
        compare_sid('\n'.join(result1), '\n'.join(result2))
    else:
        compare_sid(file1, file2)


def start(command = "all", command2 = ""):
    url = OFFICIAL_PATH
    official_files, is_match = match_file(get_text(url, 2))
    if is_match:
        for file_name in official_files:
            all_files = get_files(LOCAL_PATH, ["rules"])
            if command == "all":
                if LOCAL_PATH + file_name in all_files:
                    print("="*20)
                    print("Now comparing {0}".format(file_name))
                    # 读取文件内容
                    file1, is_text = get_text(LOCAL_PATH + file_name, 1)
                    file2, is_text = get_text(OFFICIAL_PATH + file_name,2)
                    compare_files(file1, file2)
                else:
                    print("="*20)
                    print("{0} is not in local path".format(file_name))
            elif LOCAL_PATH + command in all_files:
                print("="*20)
                print("Now comparing {0}".format(command))
                # 读取文件内容
                file1, is_text = get_text(LOCAL_PATH + command, 1)
                file2, is_text = get_text(OFFICIAL_PATH + command,2)
                compare_files(file1, file2, command2)
                break
            else:
                print("="*20)
                print("{0} is not in local path".format(command))
                break

    else:
        print("Not match!")


if __name__ == '__main__':
    if len(sys.argv)>1:
        command = sys.argv[1]
    elif len(sys.argv)>2:
        command2 = sys.argv[2]
    else:
        command = "all"
        command2 = ""
    ## 测试语句
    command = "emerging-web_specific_apps.rules"
    command2 = r"struts"

    start(command, command2)
