
Suricata
Snort
pulledpork
dalton
---


# Suricata





## 测试机

10.0.83.9机子上的suricata

root/tophant@017

setup: `/usr/local/bin/suricata`
log：`/usr/local/var/log/suricata`
rules：`/usr/local/etc/suricata/rules`

```
rules:
suricata -r ~/Ali0th/wexin.qq.pcap -v -s ali0th.rules
suricata -r ~/Ali0th/wexin.qq.pcap -v -c /usr/local/etc/suricata/suricata.yaml
log：
tail -f /usr/local/var/log/suricata/eve.json | grep ""
```



## 操作

-r 指定pcap文件
-c 指定yaml配置文件
-v 详细信息
-i 指定网口
-s 指定rules规则文件
-l 指定输出日志文件位置

### 分析流量：

`sudo /usr/local/bin/suricata -c /etc/suricata/suricata.yaml -i eth0 --init-errors-fatal`

### 分析本地的文件：

`suricata -r test.pcap -l ./ -v `

`suricata -r test.pcap -l ./ -v -s test.rules`

### 测试rules：

```s
alert icmp any any -> any any (msg:"ping test";content:"|00|";classtype:protocol-command-decode;sid:222222222;rev:4;)
```

### 禁用规则：
```
vim /etc/oinkmaster.conf
在最后处：
disablesid 2010495
```

### 通过oinkmaster修改规则：
```
sudo nano oinkmaster.conf
At the part where you can modify rules, type:
modifysid 2010495 “alert” | “drop”
```

### 通过yaml指定rules：
```
vim local.rules
vim /etc/suricata/suricata.yaml
suricata -c /etc/suricata/suricata.yaml -i wlan0
```

### 查看日志文件
```
cd /var/log/suricata
tail -n 50 stats.log
tail -f http.log stats.log
```





## Rules
`/etc/suricata/rules`

## 规则更新

emerging-attack_response.rules：更新与新增
emerging-current_events.rules：更新与新增
emerging-dns.rules：更新与新增
emerging-exploit.rules：更新与新增
emerging-info.rules：更新与新增
emerging-netbios.rules：新增
emerging-policy.rules：更新与新增
emerging-scan.rules：更新与新增
emerging-smtp.rules：更新
emerging-telnet.rules：更新
emerging-user_agents.rules：更新与新增
emerging-web_client.rules：更新与新增
emerging-web_server.rules：更新与新增
emerging-rpc.rules：全文注释，没更新
pt-rules.rules：自添加，更新与新增

进度：
emerging-web_client.rules：更新与新增
emerging-web_server.rules：更新与新增
pt-rules.rules：自添加，更新与新增







自行编写规则的一些基础说明：

sid 范围： 94640000 - 94649999
例如：94640312
9464为标识符
03 为类型号
12 为规则号

命名：
英文命名通常要表达出规则要检测的漏洞或某些行为和检测哪一部分且要去除奇异
例如：
riskIVY-PRS VULN SQLi Boolean_inject http.request.uri
riskIVY-PRS 为产品名称
VULN 为大类型
SQLi 为子类型
Boolean_inject 为规则类型
http.request.uri 为检测部分
中文名称和英文名称规范一致 如果有 CVE 或 MS/S2 编号的可将编号代入中文名称中



添加suricata rules流程：

1. 查看snort更新的社区规则
2. 漏洞利用学习，自写规则
3. 搭建漏洞验证环境
4. 漏洞复现并抓取流量，使用规则进行检测
5. 检测通过，提交到gitlab


已有suricata的规则sid：
http://git.tophant.com/gaba/nazgul-ids/raw/master/rules/sid-msg.map

经过筛选后的中文版在：
http://git.tophant.com/gaba/nazgul-ids/blob/master/suricata_sid_msg_zh_map/web_application_attack/rules.json


选用三方的 suricata 规则：

et

http://rules.emergingthreatspro.com/open/suricata-1.3-enhanced/

pt

https://github.com/ptresearch/AttackDetection


suricata规则更新流程：

1.  对比原有的规则的更新
2.  4.0新增了metadata，用python自动添加
3.  将所有的更新保存为日志下来，然后一个个查看
4.  测试或查看更新是否合理


1. 生成log文件
2. 对比打payload



### 更新 rules
```bash
sudo apt-get install oinkmaster
sudo oinkmaster -C /etc/oinkmaster.conf -o /etc/suricata/rules -u https://rules.emergingthreats.net/open/suricata-4.0/emerging.rules.tar.gz
配置新的config文件指引
sudo nano /etc/suricata/suricata.yaml
修改classification.config和reference.config
```


### wexin

原规则：

```s
alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"ET USER_AGENTS Suspicious User Agent (Microsoft Internet Explorer)"; flow: to_server,established; content:"Microsoft Internet Explorer"; depth:28; http_user_agent; content:!"bbc.co.uk|0d 0a|"; nocase; http_header; content:!"vmware.com|0d 0a|"; nocase; http_header; content:!"rc.itsupport247.net|0d 0a|"; nocase; http_header; content:!"msn.com|0d 0a|"; nocase; http_header; content:!"msn.es|0d 0a|"; nocase; http_header; content:!"live.com|0d 0a|"; nocase; http_header; content:!"gocyberlink.com|0d 0a|"; nocase; http_header; content:!"ultraedit.com|0d 0a|"; nocase; http_header; content:!"windowsupdate.com"; http_header; content:!"cyberlink.com"; http_header; content:!"lenovo.com"; http_header; content:!"itsupport247.net|0d 0a|"; nocase; http_header; content:!"msn.co.uk|0d 0a|"; http_header; threshold:type limit, track by_src, count 2, seconds 360; reference:url,doc.emergingthreats.net/bin/view/Main/2002400; classtype:trojan-activity; sid:2002400; rev:34;)
```

修改后：

```s

```



## 安装

https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Suricata_Installation

https://github.com/OISF/suricata/blob/master/doc/userguide/install.rst



## 资料

suricata源码阅读笔记

https://my.oschina.net/openadrian/blog

如何在 Linux 系统上安装 Suricata 入侵检测系统

https://linux.cn/article-6985-1.html

官方在线wiki

https://redmine.openinfosecfoundation.org/projects/suricata/wiki

明翼

https://www.jianshu.com/u/fa9c93b81e43

Suricata规则编写——常用关键字

http://blog.csdn.net/wuyangbotianshi/article/details/44775181

gaba

https://github.com/AlkenePan?tab=repositories





# Snort

## 注册

```
martin2877@foxmail.com
87878989
Oinkcode：ba930842cf134567cc8a8c31b1e9cc6deb97e434
```



## Setup

```
yum install https://www.snort.org/downloads/snort/daq-2.0.6-1.centos7.x86_64.rpm
yum install https://www.snort.org/downloads/snort/snort-2.9.11.1-1.centos7.x86_64.rpm
```



## rules

```
/etc/snort/rules
```

更新rules

```
wget https://www.snort.org/rules/snortrules-snapshot-2990.tar.gz?oinkcode=ba930842cf134567cc8a8c31b1e9cc6deb97e434 -O snortrules-snapshot-2990.tar.gz
wget https://www.snort.org/rules/snortrules-snapshot-2983.tar.gz?oinkcode=ba930842cf134567cc8a8c31b1e9cc6deb97e434 -O snortrules-snapshot-2983.tar.gz
wget https://www.snort.org/rules/snortrules-snapshot-29111.tar.gz?oinkcode=ba930842cf134567cc8a8c31b1e9cc6deb97e434 -O snortrules-snapshot-29111.tar.gz
wget https://www.snort.org/rules/snortrules-snapshot-29110.tar.gz?oinkcode=ba930842cf134567cc8a8c31b1e9cc6deb97e434 -O snortrules-snapshot-29110.tar.gz

tar -xvzf snortrules-snapshot-<version>.tar.gz -C /etc/snort/rules
```

## 资料

https://www.snort.org/documents





# pulledpork

PulledPork for Snort and Suricata rule management (from Google code)

https://github.com/shirkdog/pulledpork





# dalton

Dalton is a system that allows a user to quickly and easily run network packet captures ("pcaps") against an intrusion detection system ("IDS") sensor of his choice (e.g. Snort, Suricata) using defined rulesets and/or bespoke rules.

https://github.com/secureworks/dalton

组件有：

```
snort-2.9.11.1
suricata-current
dalton_web
suricata-3.2.4
dalton_controller
snort-2.9.9.0
dalton_redis
```

安装报错：

```shell
Step 8 : ADD https://www.snort.org/downloads/archive/snort/daq-${DAQ_VERSION}.tar.gz daq-${DAQ_VERSION}.tar.gz

ERROR: Service 'agent-snort-2.9.11' failed to build: Get https://snort-org-site.s3.amazonaws.com/production/release_files/files/000/002/146/original/daq-2.0.6.tar.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIXACIED2SPMSC7GA%2F20180209%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20180209T090155Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=93c075e10a1ad55ff175b815fcd8a4a9456c177cfd3d0c7a053def3811140833: dial tcp 54.231.82.58:443: i/o timeout
```

Fix：

将`docker-compose.yml`中的`snort-2.9.11`改为`snort-2.9.11.1`











