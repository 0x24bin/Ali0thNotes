
Suricata
Snort
pulledpork
dalton
---


# Suricata





## 测试机

10.0.83.9机子上的suricata

root/tophant@017

suricata: /usr/local/bin/suricata /usr/local/etc/suricata



log：`/usr/local/var/log/suricata`

`tail -f /usr/local/var/log/suricata/eve.json | grep ""`



rules：`/usr/local/etc/suricata/rules`

```bash
suricata -r ~/Ali0th/wexin.qq.pcap -v -c /usr/local/etc/suricata/suricata.yaml
```



## 操作

分析流量：

`sudo /usr/local/bin/suricata -c /etc/suricata/suricata.yaml -i eth0 --init-errors-fatal`

分析本地的文件：

`suricata -r test.pcap -l ./ -v `

`suricata -r test.pcap -l ./ -v -s test.rules `

测试rules：

```s
alert icmp any any -> any any (msg:"ping test";content:"|00|";classtype:protocol-command-decode;sid:222222222;rev:4;)
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



### wexin

原规则：

```bash
alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"ET USER_AGENTS Suspicious User Agent (Microsoft Internet Explorer)"; flow: to_server,established; content:"Microsoft Internet Explorer"; depth:28; http_user_agent; content:!"bbc.co.uk|0d 0a|"; nocase; http_header; content:!"vmware.com|0d 0a|"; nocase; http_header; content:!"rc.itsupport247.net|0d 0a|"; nocase; http_header; content:!"msn.com|0d 0a|"; nocase; http_header; content:!"msn.es|0d 0a|"; nocase; http_header; content:!"live.com|0d 0a|"; nocase; http_header; content:!"gocyberlink.com|0d 0a|"; nocase; http_header; content:!"ultraedit.com|0d 0a|"; nocase; http_header; content:!"windowsupdate.com"; http_header; content:!"cyberlink.com"; http_header; content:!"lenovo.com"; http_header; content:!"itsupport247.net|0d 0a|"; nocase; http_header; content:!"msn.co.uk|0d 0a|"; http_header; threshold:type limit, track by_src, count 2, seconds 360; reference:url,doc.emergingthreats.net/bin/view/Main/2002400; classtype:trojan-activity; sid:2002400; rev:34;)
```

修改后：

```bash

```



### struts2













## 安装

https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Suricata_Installation

https://github.com/OISF/suricata/blob/master/doc/userguide/install.rst


### 配置文件

/etc/suricata/suricata.yaml

#### vars

```yaml
vars:
    HOME_NET: "[192.168.122.0/24]"
    EXTERNAL_NET: "!$HOME_NET"
    HTTP_PORTS: "80"
    SHELLCODE_PORTS: "!80"
    SSH_PORTS: 22
```

`HOME_NET`变量需要指定 Suricata 检查的网络。被分配给 `EXTERNAL_NET` 变量的 `!$HOME_NET` 代表除本地网络之外的其他网络。`XXX_PORTS`变量用来辨别不同服务所用到的端口号。

#### host-os-policy

```yaml
host-os-policy:
  # These are Windows machines.
  windows: [192.168.122.0/28, 192.168.122.155]
  bsd: []
  bsd-right: []
  old-linux: []
  # Make the default policy Linux.
  linux: [0.0.0.0/0]
  old-solaris: []
  solaris: ["::1"]
  hpux10: []
  hpux11: []
  irix: []
  macos: []
  vista: []
  windows2k3: []
```

### 日志文件

/var/log/suricata/






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











