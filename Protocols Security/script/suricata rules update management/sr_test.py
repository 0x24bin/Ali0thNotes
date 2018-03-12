# -*- coding:utf8 -*-
"""
Suricata Rules Test

SR_Test is short for Suricata Rules Test, a tool to pick up and test rules.

Author : ali0th
Date   : 18/3/9
Email  : martin2877 at foxmail.com
Version: 2.0
Usage  : python SR_Test.py <keyword|sid> [sid num list]
example: 
        python SR_Test.py struts
        python SR_Test.py sid 12345 24567
        python SR_Test.py log pt-rules.rules.log
"""

import requests
import re
import os
import sys
import time
import shutil


LOCAL_PATH = r"C:/Users/muhe/Desktop/links/tophant/suricata/nazgul-ids_prs2.1/rules/" # local rules path
TEMP_PATH = r"C:/Users/muhe/Desktop/links/wirte/Ali0thNotes/Protocols Security/script/suricata rules update management/" # temp addr for file cache
LOG_PATH = TEMP_PATH
LOG_METHOD = "w"
TEMP_FILE = ""


def write_log(content):
    print(content)
    global LOG_METHOD
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    with open(LOG_PATH + "log", LOG_METHOD) as f:
        f.write(content + "\n")
    if LOG_METHOD == "w": # "w" first time to rewrite the broken log
        LOG_METHOD = "a"


def rename_log(file_name, endwith=".log"):
        # rename log
        shutil.copyfile(LOG_PATH + "log", LOG_PATH + file_name + endwith)
        os.remove(LOG_PATH + "log")

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
                with open(path) as f:
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


def progress(num, sum):
    rate = float(num) / float(sum)
    print('progress : %.1f%% %s' % (rate * 100, get_time()))


def read_log(content, method):
    """
    method:
    1. read official rule
    2. read add rule
    3. read both
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


def start(command, command2):
    write_log("#" + "="*20)
    write_log("# start search local files by {0} {1} {2}".format(command, command2, get_time()))
    all_files = get_files(LOCAL_PATH, ["rules"])

    # pick up all rules of this keyword
    if command == "keyword":
        rate = 0
        for file_path in all_files:
            rate += 1
            progress(rate, len(all_files))
            content, is_text = get_text(file_path, 1)
            if is_text :
                regex = r'.*{0}.*'.format(command2)
                result = find_regex(content, regex)
                if result:
                    write_log("#" + "="*20)
                    write_log("# found in files {0} {1}".format(file_path, get_time()))    
                    for value in result:
                        write_log(value)
            else:
                write_log("# empty file")
        rename_log(command2, ".rules")

    # pick up all rules of these sids
    elif command == "sid":
        rate = 0
        for file_path in all_files:
            rate += 1
            progress(rate, len(all_files))
            content, is_text = get_text(file_path, 1)
            regex = r"sid: ?([0-9]*?);"
            sid_list = find_regex(content, regex)
            for value in command2:
                if value in sid_list:
                    write_log("#" + "="*20)
                    write_log("# found in files {0} {1}".format(file_path, get_time()))
                    regex = r'.*sid: ?{0};.*'.format(value)
                    rule = find_regex(content, regex)[0]
                    write_log(rule)
        rename_log("sid", ".rules")

    # pick up all rules of a log file
    elif command == "log":
        content, is_text = get_text(command2, 1)
        if is_text:
            rule_list = read_log(content, 3)
            for value in rule_list:
                write_log(value + "\n")
        rename_log(command2, ".rules")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("""
    Suricata Rules Test

    SR_Test is short for Suricata Rules Test, a tool to pick up and test rules.

    Author : ali0th
    Date   : 18/3/9
    Email  : martin2877 at foxmail.com
    Version: 2.0
    Usage  : python SR_Test.py <keyword|sid> [sid num list]
    example: 
            python SR_Test.py struts
            python SR_Test.py sid 12345 24567
            python SR_Test.py log pt-rules.rules.log
            """)
    elif len(sys.argv) == 2:
        command = sys.argv[1]
        start("keyword", command)
    elif len(sys.argv) > 2 and sys.argv[1] == "sid":
        arg_list = []
        for argv in sys.argv[2:]:
            arg_list.append(argv)
        start(sys.argv[1], arg_list)
    elif len(sys.argv) > 2 and sys.argv[1] == "log":
        start(sys.argv[1], sys.argv[2])