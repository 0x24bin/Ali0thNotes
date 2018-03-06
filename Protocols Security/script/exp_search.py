import json
import sys
import pandas as pd
import urllib2

def json_data(exp_name):
    try:
        url = "http://www.exploitalert.com/api/search-exploit?name="+exp_name
        data = urllib2.urlopen(url).read()
        if ""==data:
            sys.exit("No exploits found.")
        return data
    except Exception, e:
        print e
def exp_link(exploits):
    #null
    #..
    #
    json_array = json.loads(json_data(exploits))
    print "Exploits found on the INTERNET:"+str(len(json_array))
    for item in json_array:
        item['id']="http://www.exploitalert.com/view-details.html?id="+item['id']
    return json.dumps(json_array)
def save_excel(search):
    excel_data = pd.read_json(exp_link(search))
    excel_data.to_excel(search+"_exploits.xls", index=False)
    print "See the results in "+search+"_exploits.xls."

def show_exp_detail():
    return


if __name__ == '__main__':
    save_excel(sys.argv[1])