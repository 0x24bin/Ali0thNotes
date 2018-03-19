# -*- coding:utf8 -*-
# python2


import requests
import re
import os
import sys
import shutil
from settings import *


def show(content):
    print content


def get_text(path, method, temp=TEMP_PATH):
    """
    three methods to get text
    open:     open local file
    request:  requests url
    cache:    read cache file first else download url
    """
    try:
        if method == "open":
            if os.path.exists(path):
                with open(path) as f:
                    return f.read(), True
            else:
                return [], False
        elif method == "request":
            r = requests.get(path)
            return r.text, True
        elif method == "cache":
            temp_file_name = os.path.basename(path)
            if not os.path.exists(temp):
                os.mkdir(temp)
            temp_file = temp + temp_file_name
            if os.path.exists(temp_file):
                print "file exist, opening : {0}".format(temp_file)
                return get_text(temp_file, "open")
            else:
                print "downloading : {0}".format(path)
                file_text, is_text = get_text(path, "request")
                with open(temp_file, "w") as f:
                    f.write(file_text)
                return file_text, True

    except Exception as e:
        return e, False



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
        print "Receive Offical Rules Success"
        return match, True
    else:
        return [], False


def get_files(path, rules, withpath=True):
    all_files = []
    for fpath, dirname, fnames in os.walk(path):
        for filename in fnames:
            path_name = os.path.join(fpath,filename)
            for value in rules:
                if path_name.endswith(value):
                    if withpath:
                        all_files.append(path_name)
                    else:
                        all_files.append(path_name.split("/")[-1])
    return all_files


def cuple2list(arg_cuple):
    list1 = []
    list2 = []
    for value in arg_cuple:
        list1.append(value[0])
        list2.append(value[1])
    return list1, list2

