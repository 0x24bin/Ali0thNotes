#!/usr/bin/env python
# -*- coding:utf8 -*-
# author: ali0th
# Email  : martin2877 at foxmail.com
from lib.log import read_log
from lib.base import get_files, get_text, find_regex


regex_sid = r"sid: ?([0-9]*?);"


def get_sid(content):
    global regex_sid
    sid = find_regex(content, regex_sid)
    if len(sid)>=1:
        return sid[0]
    else:
        return sid


def no_update_list(log_path):
    """
    从log文件里获取不需要更新的sid和新增的sid
    :param log_path: 文件路径
    :type log_path: str
    :return： 不需要被更新的规则的 sid 列表 和 新增规则的 sid 列表
    :rtype: list, list
    """
    no_update_list = []
    new_add_list = []
    local_files = get_files(log_path, ["log"])
    print local_files
    for file_path in local_files:
        content, is_text = get_text(file_path, "open")
        if is_text:
            no_update_list_single_file = read_log(content, "i")
            new_add_list_single_file = read_log(content, "oa")
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
    list1, list2 = no_update_list("C:/Users/muhe/Desktop/test/")
    print list1
    print len(list1)
    print list2
    print len(list2)