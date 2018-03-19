#!/usr/bin/env python
# -*- coding:utf8 -*-
# author: ali0th
# Email  : martin2877 at foxmail.com
"""
Suricata Rules Compare
SR_Compare is short for Suricata Rules compare, a tool to compare rules between local and official.

COMPARE
python srum.py -c --all
python srum.py -c -f emerging-icmp.rules
python srum.py -c -f <file> -k <keyword>
python srum.py -c -f emerging-web_specific_apps.rules -k struts

"""
from optparse import OptionGroup, OptionParser
import sys
from settings import *
from lib.utils import *
from lib.log import *
from lib.base import *

regex_sid_rev = r"sid: ?([0-9]*?);.*?rev: ?([0-9]*?);"

def compare_sid(content1, content2):
    write_log("start compare_sid", True)
    # get sid and rev
    global regex_sid_rev
    sid_list1 = find_regex(content1, regex_sid_rev)
    sid_list2 = find_regex(content2, regex_sid_rev)
    # compare
    write_log("start compare sid_list1 to 2, sid_list1 len is {0}, sid_list2 len is {1}".format(len(sid_list1),len(sid_list2)), True)
    for sid1 in sid_list1:
        for sid2 in sid_list2:
            if sid1[0] == sid2[0] and sid1[1] != sid2[1]: # compare sid and rev, if rev is equal, they are same.
                regex = r'.*sid: ?{0};.*'.format(sid1[0])
                write_log("="*20)
                write_log("local : {0}\n".format(find_regex(content1, regex)[0]))
                write_log("official : {0}\n".format(find_regex(content2, regex)[0]))
    # add
    write_log("start compare sid_list2 to 1", True)
    sid_list1_1, nothing = cuple2list(sid_list1)
    sid_list2_1, nothing = cuple2list(sid_list2)
    for sid2 in sid_list2_1:
        if sid2 not in sid_list1_1:
            regex = r'.*sid: ?{0};.*'.format(sid2)
            write_log("="*20)
            write_log("add : {0}\n".format(find_regex(content2, regex)[0]))



def compare_files_text(file1, file2, regex=""):
    """
    if regex exists, compare text of  two files, using the regex to find the specified content first. And then compare their sid.
    if not, compare two files by their sid.
    """
    if regex:
        write_log("start finding regex : {0} ,it may spend times".format(regex), True)
        result1 = find_regex(file1, regex)
        result2 = find_regex(file2, regex)
        compare_sid('\n'.join(result1), '\n'.join(result2))
    else:
        compare_sid(file1, file2)


def compare_file(file_name, regex):
    file1, is_text1 = get_text(LOCAL_PATH + file_name, "open")
    file2, is_text2 = get_text(OFFICIAL_PATH + file_name,"cache")
    if is_text1 and is_text2:
        compare_files_text(file1, file2, regex)
        rename_log(file_name)
    else:
        write_log("Cannot open {0} file1 {1} file2 {2}".format(file_name, is_text1, is_text2), True)
    write_log("process end", True)


def compare(options):
    regex = ""
    if options.keyword: regex = r'.*{0}.*'.format(options.keyword)
    
    local_files = get_files(LOCAL_PATH, ["rules"], False)
    if options.all:
        write_log("start search official files", True)
        official_files, is_match = match_file(get_text(OFFICIAL_PATH, "request"))
        if is_match:
            for file_name in official_files:
                if file_name in local_files:
                    compare_file(file_name, regex)

    elif options.file:
        if options.file in local_files:
            compare_file(options.file, regex)
        else:
            write_log("Cannot find {0}".format(options.file), True)


def cmdline_parse():
    usage = """ python %prog -c [options] [action]
example:
        python srum.py -c --all
        python srum.py -c -f emerging-icmp.rules
        python srum.py -c -f <file> -k <keyword>
        python srum.py -c -f emerging-web_specific_apps.rules -k struts
    """
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--compare', dest="compare", default=False, action='store_true', help='compare module')
    action = OptionGroup(parser, "ACTION")
    action.add_option('--all', dest="all", action='store_true', help='all rules file')
    action.add_option('-f', dest="file", type='string', help='single rule file')
    action.add_option('-k', dest="keyword", type='string', help='assign keyword')
    parser.add_option_group(action)

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    options, args = parser.parse_args()

    if not options.compare:
        print "-c is in need"
    if not (options.all or options.file):
        print "one of --all/-f is in need"
    return options, args

def main():
    options, args = cmdline_parse()
    if options.compare:
        compare(options)

if __name__ == '__main__':
    main()