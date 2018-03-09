# -*- coding:utf8 -*-
"""
Suricata Rules Test

SR_Test is short for Suricata Rules Test, a tool to test rules.

Author : ali0th
Date   : 18/3/9
Email  : martin2877 at foxmail.com
Version: 2.0
Usage  : python SR_Test.py [rules file] [keyword]
example: 
python SR_Test.py struts
python SR_Test.py sid 12345 24567
"""

import requests
import re
import os
import sys
import time
import shutil

OFFICIAL_PATH = r'https://rules.emergingthreats.net/open/suricata-4.0/rules/' # official rules addr
LOCAL_PATH = r"C:/Users/muhe/Desktop/links/tophant/suricata/nazgul-ids_prs2.1/rules/" # local rules path
TEMP_PATH = r"C:/Users/muhe/Desktop/links/wirte/Ali0thNotes/Protocols Security/script/suricata rules update management/" # temp addr for file cache
LOG_PATH = TEMP_PATH
LOG_METHOD = "w"
TEMP_FILE = ""


def write_log(content):
    print(content)
    global LOG_METHOD
    with open(LOG_PATH + "log", LOG_METHOD) as f:
        f.write(content + "\n")
    if LOG_METHOD == "w": # "w" first time to rewrite the broken log
        LOG_METHOD = "a"


def rename_log(file_name, endwith=".log"):
        # rename log
        shutil.copyfile(LOG_PATH + "log", LOG_PATH + file_name + endwith)
        os.remove(LOG_PATH + "log")


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
            temp_file = TEMP_PATH + temp_file_name
            if os.path.exists(temp_file):
                write_log("# file exist, opening : {0}".format(temp_file) )
                return get_text(temp_file, 1)
            else:
                write_log("# downloading : {0}".format(path) )
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



def start(command, command2):
    print(command,command2)
    write_log("# ="*20)
    write_log("# start search local files {0}".format(get_time()))
    all_files = get_files(LOCAL_PATH, ["rules"]) 

    # pick up all rules of this keyword
    if command == "keyword":
        for file_name in all_files:
            content, is_text = get_text(LOCAL_PATH + file_name, 1)
            if is_text :
                regex = r'.*{0}.*'.format(regex)
                result = find_regex(content, regex)
                if result:
                    for value in result:
                        write_log(value)
            else:
                write_log("# empty file")
        rename_log(command)
    # pick up all rules of these sids
    elif command == "sid":
        for file_name in all_files:
            content, is_text = get_text(LOCAL_PATH + file_name, 1)
            regex = r"sid: ?([0-9]*?);"
            sid_list = find_regex(content, regex)
            for value in command2:
                if value in sid_list:
                    regex = r'.*sid: ?{0};.*'
                    rule = find_regex(content, regex)[0]
                    write_log(rule)
        rename_log("sid", ".rules")



if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("""
    Suricata Rules Test
    SR_Test is short for Suricata Rules Test, a tool to test rules.

    Author : ali0th
    Date   : 18/3/9
    Email  : martin2877 at foxmail.com
    Version: 2.0
    Usage  : python SR_Test.py <keyword> [sid]
    example: 
        python SR_Test.py struts
        python SR_Test.py sid 12345 24567
            """)
    elif len(sys.argv) == 2:
        command = sys.argv[1]
        start("keyword", command)
    elif len(sys.argv) > 2 and sys.argv[1] == "sid":
        arg_list = []
        for argv in sys.argv[2:]:
            arg_list.append(argv)
        start(sys.argv[1], arg_list)