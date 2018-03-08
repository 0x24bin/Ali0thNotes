# -*- coding:utf8 -*-
"""
Suricata Rules Update Management

SRUM is short for Suricata Rules Update Management , a tool to compare and update rules between local and official.

Author : ali0th
Date   : 18/3/7
Email  : martin2877 at foxmail.com

Usage  : python srum.py [rules file] [keyword]
example: python srum.py emerging-web_specific_apps.rules struts

"""

import requests
import re
import os
import sys
import time

OFFICIAL_PATH = r'https://rules.emergingthreats.net/open/suricata-4.0/rules/' # official rules addr
LOCAL_PATH = r"C:/Users/muhe/Desktop/links/tophant/suricata/nazgul-ids_prs2.1/rules/" # local rules path
TEMP_PATH = r"C:/Users/muhe/Desktop/links/wirte/Ali0thNotes/Protocols Security/script/suricata rules update management/" # temp addr for file cache
LOG_PATH = TEMP_PATH
LOG_METHOD = "w"


def write_log(content):
    print(content)
    global LOG_METHOD
    with open(LOG_PATH + "log", LOG_METHOD) as f:
        f.write(content + "\n")
    if LOG_METHOD == "w": # "w" first time
        LOG_METHOD = "a"


def get_text(path, method):
    """
    three methods to get text
    1. open local file
    2. requests url
    3. read temp file first else download url
    """
    try:
        if method == 1:
            with open(path) as f:
                return f.read(), True
        elif method == 2:
            r = requests.get(path, stream=True)
            return r.text, True
        elif method == 3: 
            temp_file_name = os.path.basename(path)
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


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def find_regex(content, regex):
    pattern = re.compile(regex,re.I)
    match = pattern.findall(str(content))
    return match


def progress(num, sum):
    rate = float(num) / float(sum)
    print('progress : %.2f%% \n' % (rate))
    

def match_file(content):
    """
    find official file
    """
    regex = r'<a href="[^?^/].*?">(.*?)</a>'
    match = find_regex(content, regex)
    if match:
        write_log("Receive Offical Rules Success {0}".format(get_time()))
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


def compare_files(file1, file2, regex=""):
    """
    if regex exists, compare text of  two files, using the regex to find the specified content first. And then compare their sid.
    if not, compare two files by their sid.
    """

    def compare_sid(content1, content2):
        write_log("="*20)
        write_log("start compare_sid  {0}".format(get_time()))
        regex = r'sid:([0-9]*?);'
        sid_list1 = find_regex(content1, regex)
        sid_list2 = find_regex(content2, regex)
        write_log("="*20)
        write_log("start compare sid_list1 to 2, sid_list1 len is {0}, sid_list2 len is {1} {2}".format(len(sid_list1),len(sid_list2),get_time()))
        for sid1 in sid_list1:
            if sid1 in sid_list2:
                regex = r'.*sid:{0};.*'.format(sid1)
                write_log("="*20)
                write_log("local : {0}\n".format(find_regex(content1, regex)[0]))
                write_log("official : {0}\n".format(find_regex(content2, regex)[0]))
        write_log("="*20)
        write_log("start compare sid_list2 to 1  {0}".format(get_time()))
        for sid2 in sid_list2:
            if sid2 not in sid_list1:
                regex = r'.*sid:{0};.*'.format(sid2)
                write_log("="*20)
                write_log("add : {0}\n".format(find_regex(content2, regex)[0]))
        write_log("="*20)
        write_log("process end {0}".format(get_time()))


    if regex:
        regex = r'.*{0}.*'.format(regex)
        write_log("="*20)
        write_log("start finding regex : {0} ,it may spend times {1}".format(regex , get_time()))
        result1 = find_regex(file1, regex)
        result2 = find_regex(file2, regex)
        compare_sid('\n'.join(result1), '\n'.join(result2))
    else:
        compare_sid(file1, file2)


def start(command = "all", command2 = ""):
    url = OFFICIAL_PATH
    official_files, is_match = match_file(get_text(url, 2))
    write_log("="*20)
    write_log("start search files {0}".format(get_time()))
    all_files = get_files(LOCAL_PATH, ["rules"])
    write_log("end search files {0}".format(get_time()))    
    if is_match:
        if command == "all":
            for file_name in official_files:
                if LOCAL_PATH + file_name in all_files:
                    write_log("="*20)
                    write_log("Now comparing {0}".format(file_name))
                    # read file content
                    file1, is_text1 = get_text(LOCAL_PATH + file_name, 1)
                    file2, is_text2 = get_text(OFFICIAL_PATH + file_name,3)
                    if is_text1 and is_text2:
                        compare_files(file1, file2)
                    else:
                        write_log("empty file")
                else:
                    write_log("="*20)
                    write_log("{0} is not in local path".format(file_name))
        elif LOCAL_PATH + command in all_files:
            write_log("="*20)
            write_log("Now comparing {0} {1}".format(command, command2))
            # read file content
            write_log("="*20)
            write_log("Now read file 1 {0} {1}".format(command, get_time()))
            file1, is_text1 = get_text(LOCAL_PATH + command, 1)
            write_log("="*20)
            write_log("Now read file 2 {0} {1}".format(command, get_time()))
            file2, is_text2 = get_text(OFFICIAL_PATH + command,3)
            if is_text1 and is_text2:
                compare_files(file1, file2, command2)
            else:
                write_log("empty file")
        else:
            write_log("="*20)
            write_log("{0} is not in local path".format(command))
    else:
        write_log("No official files!")


if __name__ == '__main__':
    if len(sys.argv)>1:
        command = sys.argv[1]
    elif len(sys.argv)>2:
        command2 = sys.argv[2]
    else:
        command = "all"
        command2 = ""

    command = "emerging-web_specific_apps.rules"    ## 测试语句
    command2 = r"struts"    ## 测试语句

    start(command, command2)
