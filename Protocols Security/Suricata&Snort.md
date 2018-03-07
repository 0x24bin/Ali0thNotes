
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

常用:



分析流量：

`sudo /usr/local/bin/suricata -c /etc/suricata/suricata.yaml -i eth0 --init-errors-fatal`

分析本地的文件：

`suricata -r test.pcap -l ./ -v `

`suricata -r test.pcap -l ./ -v -s test.rules`

测试rules：

```s
alert icmp any any -> any any (msg:"ping test";content:"|00|";classtype:protocol-command-decode;sid:222222222;rev:4;)
```

禁用规则：
```
vim /etc/oinkmaster.conf
在最后处：
disablesid 2010495
```

通过oinkmaster修改规则：
```
sudo nano oinkmaster.conf
At the part where you can modify rules, type:
modifysid 2010495 “alert” | “drop”
```

通过yaml指定rules：
```
vim local.rules
vim /etc/suricata/suricata.yaml
suricata -c /etc/suricata/suricata.yaml -i wlan0
```


## Rules
`/etc/suricata/rules`
### 修改流程

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



原suricata往4.0更新流程：

1.  对比原有的规则的更新
2.  4.0新增了metadata，用python自动添加
3.  将所有的更新保存为日志下来，然后一个个查看
4.  测试或查看更新是否合理






### wexin

原规则：

```s
alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"ET USER_AGENTS Suspicious User Agent (Microsoft Internet Explorer)"; flow: to_server,established; content:"Microsoft Internet Explorer"; depth:28; http_user_agent; content:!"bbc.co.uk|0d 0a|"; nocase; http_header; content:!"vmware.com|0d 0a|"; nocase; http_header; content:!"rc.itsupport247.net|0d 0a|"; nocase; http_header; content:!"msn.com|0d 0a|"; nocase; http_header; content:!"msn.es|0d 0a|"; nocase; http_header; content:!"live.com|0d 0a|"; nocase; http_header; content:!"gocyberlink.com|0d 0a|"; nocase; http_header; content:!"ultraedit.com|0d 0a|"; nocase; http_header; content:!"windowsupdate.com"; http_header; content:!"cyberlink.com"; http_header; content:!"lenovo.com"; http_header; content:!"itsupport247.net|0d 0a|"; nocase; http_header; content:!"msn.co.uk|0d 0a|"; http_header; threshold:type limit, track by_src, count 2, seconds 360; reference:url,doc.emergingthreats.net/bin/view/Main/2002400; classtype:trojan-activity; sid:2002400; rev:34;)
```

修改后：

```s

```



### struts2


```s
2024468 || ET WEB_SPECIFIC_APPS OGNL Expression Injection (CVE-2017-9791) || cve,2017-9791 || url,securityonline.info/tutorial-cve-2017-9791-apache-struts2-s2-048-remote-code-execution-vulnerability/
2024663 || ET EXPLOIT Apache Struts 2 REST Plugin XStream RCE (ProcessBuilder) || url,lgtm.com/blog/apache_struts_CVE-2017-9805_announcement || cve,2017-9805
2024664 || ET EXPLOIT Apache Struts 2 REST Plugin XStream RCE (Runtime.Exec) || url,lgtm.com/blog/apache_struts_CVE-2017-9805_announcement || cve,2017-9805
2024668 || ET EXPLOIT Apache Struts 2 REST Plugin ysoserial Usage (B64) 1 || url,lgtm.com/blog/apache_struts_CVE-2017-9805_announcement || cve,2017-9805
2024669 || ET EXPLOIT Apache Struts 2 REST Plugin ysoserial Usage (B64) 2 || url,lgtm.com/blog/apache_struts_CVE-2017-9805_announcement || cve,2017-9805
2024670 || ET EXPLOIT Apache Struts 2 REST Plugin ysoserial Usage (B64) 3 || url,lgtm.com/blog/apache_struts_CVE-2017-9805_announcement || cve,2017-9805
2024671 || ET EXPLOIT Apache Struts 2 REST Plugin (B64) 4 || url,lgtm.com/blog/apache_struts_CVE-2017-9805_announcement || cve,2017-9805
2024672 || ET EXPLOIT Apache Struts 2 REST Plugin (B64) 5 || url,lgtm.com/blog/apache_struts_CVE-2017-9805_announcement || cve,2017-9805
2024673 || ET EXPLOIT Apache Struts 2 REST Plugin (B64) 6 || url,lgtm.com/blog/apache_struts_CVE-2017-9805_announcement || cve,2017-9805
2024674 || ET EXPLOIT Apache Struts 2 REST Plugin (Runtime.Exec) || url,lgtm.com/blog/apache_struts_CVE-2017-9805_announcement || cve,2017-9805
2024675 || ET EXPLOIT Apache Struts 2 REST Plugin (ProcessBuilder) || url,lgtm.com/blog/apache_struts_CVE-2017-9805_announcement || cve,2017-9805
2024814 || ET EXPLOIT Likely Struts S2-053-CVE-2017-12611 Exploit Attempt M1
2024815 || ET EXPLOIT Likely Struts S2-053-CVE-2017-12611 Exploit Attempt M2
2024843 || ET SCAN struts-pwn User-Agent || url,paladion.net/paladion-cyber-labs-discovers-a-new-ransomware/ || cve,2017-9805 || url,github.com/mazen160/struts-pwn_CVE-2017-9805/blob/master/struts-pwn.py
```











## 安装

https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Suricata_Installation

https://github.com/OISF/suricata/blob/master/doc/userguide/install.rst

### 更新 rules
```bash
sudo apt-get install oinkmaster
sudo oinkmaster -C /etc/oinkmaster.conf -o /etc/suricata/rules -u https://rules.emergingthreats.net/open/suricata-4.0/emerging.rules.tar.gz
配置新的config文件指引
sudo nano /etc/suricata/suricata.yaml
修改classification.config和reference.config
```

### 配置文件

/etc/suricata/suricata.yaml

### 日志文件
```
cd /var/log/suricata
tail -n 50 stats.log
tail -f http.log stats.log
```

## 资料

suricata源码阅读笔记

https://my.oschina.net/openadrian/blog

如何在 Linux 系统上安装 Suricata 入侵检测系统

https://linux.cn/article-6985-1.html

官方在线wiki

https://redmine.openinfosecfoundation.org/projects/suricata/wiki


https://www.jianshu.com/u/fa9c93b81e43

Suricata规则编写——常用关键字

http://blog.csdn.net/wuyangbotianshi/article/details/44775181








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











