
import re
TEMP_PATH = r"C:/Users/muhe/Desktop/links/wirte/Ali0thNotes/Protocols Security/script/suricata rules update management/" # temp addr for file cache

def find_regex(content, regex):
    pattern = re.compile(regex,re.I)
    match = pattern.findall(str(content))
    return match

with open(TEMP_PATH + "emerging-web_specific_apps.rules", "r") as f:
    regex = r"sid:([0-9]*?);.*?rev:([0-9]*?);"
    match = find_regex(f.read(), regex)
    # print(match)
    for value in match:
        print(value)