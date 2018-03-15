"""
author: ali0th
email: muhe.ye@tophant.com
date: 2018/3/14
"""
import os
import shutil
import sys
from libsimba import Rules


DEBUG = True

class LogRules:

    # 规则 匹配official 和 add
    _rule_filter_regex = r"^\s*(?:add|official){1} :\s*(?:alert|drop|log|pass|reject|sdrop|activate|dynamic)\s.+;\s*\)\s*$"
    _rule_filter = re.compile(_rule_filter_regex)

    # 规则 匹配official
    _rule_official_filter_regex = r"^\s*official :\s*(?:alert|drop|log|pass|reject|sdrop|activate|dynamic)\s.+;\s*\)\s*$"
    _rule_official_filter = re.compile(_rule_official_filter_regex)

    # 规则 匹配add
    _rule_add_filter_regex = r"^\s*add :\s*(?:alert|drop|log|pass|reject|sdrop|activate|dynamic)\s.+;\s*\)\s*$"
    _rule_add_filter = re.compile(_rule_add_filter_regex)

    # 提取规则中的 sid
    _rule_sid_filter_regex = "sid:\s*([0-9]{7,10});"
    _rule_sid_filter = re.compile(_rule_sid_filter_regex)

    def __init__(self, function_logger=None, operation_logger=None):
        """
        初始化
        :param function_logger: 日志处理对象
        :param operation_logger: 规则操作日志
        :type function_logger: Logger
        :type operation_logger: Logger
        """
        self.function_logger = function_logger
        self.operation_logger = operation_logger
        self.rules = []
        self.rules_dirs = []
        self.rule_files = []
        self.file_sids_map = {}
        self.sid_rules_index = {}

    def load_rules_file_from_directory(self, directory_path):
        """
        遍历目录 按照后缀提取 所有规则文件
        :param directory_path: 存放由规则的目录(绝对路径)
        :type directory_path: str
        :return： 是否遍历正常完成
        :rtype: bool
        """
        try:
            if not isinstance(directory_path, str):
                raise Exception("directory_path type error need str")
            if not os.path.exists(directory_path):
                raise Exception("directory_path is not exists")
            # 遍历目录 提取规则文件
            for dir_path, dir_names, file_names in os.walk(directory_path):
                # BUG fixed
                self.rules_dirs.append(dir_path)
                for filename in file_names:
                    # 规则文件要以 .log 结尾
                    if filename.endswith(".log"):
                        self.rule_files.append("{path}/{filename}".format(path=dir_path, filename=filename))
        except Exception as e:
            self.function_log(str(e))
            return False
        return True



    def load_rules(self, dir_or_file):
        """
        从目录或文件加载规则
        :param dir_or_file: 目录或文件
        :type dir_or_file: str
        :return: 是否成功加载规则
        :rtype: bool
        """
        if os.path.isdir(dir_or_file):
            self.load_rules_file_from_directory(dir_or_file)
        elif os.path.isfile(dir_or_file):
            if os.path.isabs(dir_or_file):
                self.rule_files.append(dir_or_file)
            else:
                try:
                    abs_path = os.path.abspath(dir_or_file)
                    self.rule_files.append(abs_path)
                except Exception as error:
                    self.function_log(str(error))
                    return False
        if not len(self.rule_files):
            self.function_log("zero rule file loaded")
            return False
        # 已经将全部文件列表加载完毕 依次加载文件中的规则 load_rule_from_file
        for rule_file in self.rule_files:
            self.load_rule_from_file(rule_file)


class update_by_log:
    def __init__(self, log_path):
        self.log_path = log_path
        self.update_sid = []
        self.add_sid = []
        self._init()

    def __init(self):
        self.log_rules = LogRules()
        print "[*] loading log rules: {}".format(self.log_path)
        self.local_rules.load_rules(self.log_path)
        self.update_sid = self.log_rules.update_sid()
        self.add_sid = self.log_rules.add_sid()


if __name__ == "__main__":
    # update = update_by_log("/home/muhe/Desktop/newrules/")
    update = update_by_log("C:/Users/muhe/Desktop/links/wirte/Ali0thNotes/Protocols Security/script/suricata rules update management/newlog/")
    print update.update_sid()
    print update.add_sid()
    print "DONE!"






























