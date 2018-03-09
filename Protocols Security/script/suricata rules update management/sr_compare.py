# -*- coding:utf8 -*-
"""
Suricata Rules Compare

SR_Compare is short for Suricata Rules compare, a tool to compare rules between local and official.

Author : ali0th
Date   : 18/3/7
Email  : martin2877 at foxmail.com
Version: 2.0
Usage  : python SR_Compare.py [rules file] [keyword]
example: python SR_Compare.py emerging-web_specific_apps.rules struts

"""

import requests
import re
import os
import sys
import time
import shutil


OFFICIAL_PATH = r'https://rules.emergingthreats.net/open/suricata-4.0/rules/' # official rules addr
PT_PATH = r'https://github.com/ptresearch/AttackDetection/blob/master/pt.rules.tar.gz' # pt rules addr
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


def rename_log(file_name):
        # rename log
        shutil.copyfile(LOG_PATH + "log", LOG_PATH + file_name + ".log")
        os.remove(LOG_PATH + "log")


def cuple2list(arg_cuple):
    list1 = []
    list2 = []
    for value in arg_cuple:
        list1.append(value[0])
        list2.append(value[1])
    return list1, list2


def compare_files(file1, file2, regex=""):
    """
    if regex exists, compare text of  two files, using the regex to find the specified content first. And then compare their sid.
    if not, compare two files by their sid.
    """

    def compare_sid(content1, content2):
        write_log("="*20)
        write_log("start compare_sid  {0}".format(get_time()))
        # get sid and rev
        regex = r"sid: ?([0-9]*?);.*?rev: ?([0-9]*?);"
        sid_list1 = find_regex(content1, regex)
        sid_list2 = find_regex(content2, regex)
        # compare
        write_log("="*20)
        write_log("start compare sid_list1 to 2, sid_list1 len is {0}, sid_list2 len is {1} {2}".format(len(sid_list1),len(sid_list2),get_time()))
        for sid1 in sid_list1:
            for sid2 in sid_list2:
                if sid1[0] == sid2[0] and sid1[1] != sid2[1]: # compare sid and rev, if rev is equal, they are same.
                    regex = r'.*sid: ?{0};.*'.format(sid1[0])
                    write_log("="*20)
                    write_log("local : {0}\n".format(find_regex(content1, regex)[0]))
                    write_log("official : {0}\n".format(find_regex(content2, regex)[0]))
        # add
        write_log("="*20)
        write_log("start compare sid_list2 to 1  {0}".format(get_time()))
        sid_list1_1, nothing = cuple2list(sid_list1)
        sid_list2_1, nothing = cuple2list(sid_list2)
        for sid2 in sid_list2_1:
            if sid2 not in sid_list1_1:
                regex = r'.*sid: ?{0};.*'.format(sid2)
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
    write_log("="*20)
    write_log("start search local files {0}".format(get_time()))
    all_files = get_files(LOCAL_PATH, ["rules"]) 
    if command == "all":
        write_log("="*20)
        write_log("start search official files {0}".format(get_time()))
        official_files, is_match = match_file(get_text(OFFICIAL_PATH, 2))
        if not is_match:
            write_log("No official files!")
            return
        for file_name in official_files:
            if LOCAL_PATH + file_name in all_files:
                write_log("="*20)
                write_log("Now comparing {0}".format(file_name))
                # read file content
                file1, is_text1 = get_text(LOCAL_PATH + file_name, 1)
                file2, is_text2 = get_text(OFFICIAL_PATH + file_name,3)
                if is_text1 and is_text2:
                    compare_files(file1, file2)
                    rename_log(file_name)
                else:
                    write_log("empty file")
            else:
                write_log("="*20)
                write_log("{0} is not in local path".format(file_name))

    elif command != "pt" and LOCAL_PATH + command in all_files:
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
            rename_log(command)
        else:
            write_log("empty file")

    elif command == "pt":
        
        # (下载tar.gz,解压它取出其中的文件，然后删除tar.gz(未实现)  # get_text(PT_PATH, 3))

        commnad = "pt-rules.rules"
        if LOCAL_PATH + commnad in all_files:
            write_log("="*20)
            write_log("Now comparing {0}".format(commnad))
            # read file content
            file1, is_text1 = get_text(LOCAL_PATH + commnad, 1)
            file2, is_text2 = get_text(OFFICIAL_PATH + commnad,3)
            if is_text1 and is_text2:
                compare_files(file1, file2)
                rename_log(commnad)
            else:
                write_log("empty file")
        else:
            write_log("="*20)
            write_log("{0} is not in local path".format(commnad))
    else:
        write_log("="*20)
        write_log("{0} is not in local path".format(command))



if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("""
    Suricata Rules Compare

    SR_Compare is short for Suricata Rules compare, a tool to compare rules between local and official.

    Author : ali0th
    Date   : 18/3/7
    Email  : martin2877 at foxmail.com
    Version: 2.0
    Usage  : python SR_Compare.py [rules file] [keyword]
    example: 
    
    python SR_Compare.py emerging-web_specific_apps.rules struts
    
    compare all file : python SR_Compare.py all

    compare pt-rules.rules : python SR_Compare.py pt
    
    test : python SR_Compare.py test

            """)
    elif len(sys.argv) == 2:
        command = sys.argv[1]
        if command == "test":
            print("start test using emerging-web_specific_apps.rules struts")
            command = "emerging-web_specific_apps.rules"    ## 测试语句
            command2 = r"struts"    ## 测试语句
            start(command, command2)
        elif command == "pt":
            start(command)
        elif command == "all":
            start()
    elif len(sys.argv) == 3:
        command = sys.argv[1]
        command2 = sys.argv[2]
        start(command, command2)