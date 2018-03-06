## Bro

## 常用语句

```
export PATH=/usr/local/bro/bin:$PATH
tcpdump -i ens33 -s 0 -w mypackets.trace
bro -C -r icmp_tunnel.pcap ~/bro-scripts/entrypoint.bro
```

### 资料：

github：

<https://github.com/bro/bro>

官网：

<https://www.bro.org>

基于bro的计算机入侵取证实战分析:

<http://www.freebuf.com/articles/system/135843.html>

bro开发跟进：

<https://bro-tracker.atlassian.net/secure/Dashboard.jspa>

使用bro

<https://www.bro.org/sphinx/index.html#using-bro>



### Bro命令



```
[root@localhost pcap]# bro -h
bro version 2.5-372
usage: bro [options] [file ...]
    <file>                         | policy file, or read stdin
    -a|--parse-only                | exit immediately after parsing scripts
    -b|--bare-mode                 | don't load scripts from the base/ directory
    -d|--debug-policy              | activate policy file debugging
    -e|--exec <bro code>           | augment loaded policies by given code
    -f|--filter <filter>           | tcpdump filter
    -g|--dump-config               | dump current config into .state dir
    -h|--help|-?                   | command line help
    -i|--iface <interface>         | read from given interface
    -p|--prefix <prefix>           | add given prefix to policy file resolution
    -r|--readfile <readfile>       | read from given tcpdump file
    -s|--rulefile <rulefile>       | read rules from given file
    -t|--tracefile <tracefile>     | activate execution tracing
    -v|--version                   | print version and exit
    -w|--writefile <writefile>     | write to given tcpdump file
    -x|--print-state <file.bst>    | print contents of state file
    -C|--no-checksums              | ignore checksums
    -F|--force-dns                 | force DNS
    -G|--load-seeds <file>         | load seeds from given file
    -H|--save-seeds <file>         | save seeds to given file
    -I|--print-id <ID name>        | print out given ID
    -N|--print-plugins             | print available plugins and exit (-NN for verbose)
    -P|--prime-dns                 | prime DNS
    -Q|--time                      | print execution time summary to stderr
    -R|--replay <events.bst>       | replay events
    -S|--debug-rules               | enable rule debugging
    -T|--re-level <level>          | set 'RE_level' for rules
    -U|--status-file <file>        | Record process status in file
    -W|--watchdog                  | activate watchdog timer
    -X|--broxygen <cfgfile>        | generate documentation based on config file
    --pseudo-realtime[=<speedup>]  | enable pseudo-realtime for performance evaluation (default 1)
    $BROPATH                       | file search path (.:/usr/local/bro/share/bro:/usr/local/bro/share/bro/policy:/usr/local/bro/share/bro/site)
    $BRO_PLUGIN_PATH               | plugin search path (/usr/local/bro/lib/bro/plugins)
    $BRO_PLUGIN_ACTIVATE           | plugins to always activate ()
    $BRO_PREFIXES                  | prefix list ()
    $BRO_DNS_FAKE                  | disable DNS lookups (off)
    $BRO_SEED_FILE                 | file to load seeds from (not set)
    $BRO_LOG_SUFFIX                | ASCII log file extension (.log)
    $BRO_PROFILER_FILE             | Output file for script execution statistics (not set)
    $BRO_DISABLE_BROXYGEN          | Disable Broxygen documentation support (not set)
```



### 搭建Bro

#### 使用centos

```
redhat:RHEL/Fedora/centos
debain:debain/ubuntu
FreeBSD
```

#### 安装环境：

```
sudo yum install cmake make gcc gcc-c++ flex bison libpcap-devel openssl-devel python-devel swig zlib-devel
```

#### 安装bro：

```
git clone --recursive git://git.bro.org/bro
./configure
make
make install
```

#### 启动：

```
先：
export PATH=/usr/local/bro/bin:$PATH
然后才能：
broctl
bro
```

#### 抓包：

```
tcpdump -i eth0 -s 0 -w mypackets.trace
-s 0 抓取所有数据包，有些版本不支持使用 -s 65535替代
我这里为
tcpdump -i ens33 -s 0 -w mypackets.trace
```

#### tcpdump：

`https://www.cnblogs.com/ggjucheng/archive/2012/01/14/2322659.html`

#### 分析包：

```
然后用默认的规则分析数据包
bro -r mypackets.trace
或者你对更多的检测感兴趣，可以加载bro脚本分析
bro -r mypackets.trace myscript.bro

bro -r mypackets.trace /usr/local/bro/share/bro/policy/bro-scripts/tophant.entrypoint.bro
```

#### 分析结果：

```
.
├── ./conn.log
├── ./dhcp.log
├── ./dns.log
├── ./mypackets.trace
├── ./packet_filter.log
├── ./reporter.log
└── ./weird.log
```



```
conn.log:
Contains an entry for every connection seen on the wire, with basic properties such as time and duration, originator and responder IP addresses, services and ports, payload size, and much more. This log provides a comprehensive record of the network’s activity.

notice.log:
Identifies specific activity that Bro recognizes as potentially interesting, odd, or bad. In Bro-speak, such activity is called a “notice”.
```



#### 安装Kafka插件：

##### 官方流程（有点问题）

https://www.bro.org/sphinx/components/bro-plugins/kafka/README.html

##### Logging Bro Output to Kafka

https://metron.apache.org/current-book/metron-sensors/bro-plugin-kafka/index.html

##### 以下为自己成功的安装过程：

plugins

https://github.com/bro/bro-plugins/

下载bro-plugins:

`# wget https://github.com/bro/bro-plugins/archive/v0.5.zip -O bro-plugins.zip`

解压安装：

```
# unzip bro-plugins.zip
# ./configure --bro-dist=$BRO_SRC
注意这里的$BRO_SRC为bro源文件目录，如我放在/root/bro，则一句为./configure --bro-dist=/root/bro
# make
# sudo make install
```

验证安装成功：

```
# bro -N Bro::Kafka
Bro::Kafka - Writes logs to Kafka (dynamic, version 0.1)
```

启动kafka:

```
bin/zookeeper-server-start.sh config/zookeeper.properties &

bin/kafka-server-start.sh config/server.properties &
```



### 日志：

```
dpd.log 　　      协议在非标准端口上遇到的摘要
dns.log 　　      所有DNS活动
ftp.log 　　      一个日志的FTP会话级别的活动
files.log 　　    摘要通过网络传输的文件。这些信息是聚合不同的协议,包括HTTP、FTP、SMTP
http.log 　　     总结所有的HTTP请求的回复
known_certs.log 　使用SSL证书
smtp.log 　　     SMTP活动的一个总结
ssl.log 　　      SSL会话的记录,包括所使用的证书
weird.log 　　    一个意想不到的协议级活动的日志。只要bro协议分析遇到不符合期望的(如:一个RFC违规)日志会记录在这个文件中。注意,在实践中,现实世界的网络往往表现出大量的“杂质”,通常是不值得跟进。 
```

所有日志：

<https://www.bro.org/sphinx/script-reference/log-files.html>



#### 日志查看：

使用bro-cut

`https://www.bro.org/sphinx/components/bro-aux/README.html#bro-cut`



```
[root@localhost ftp]# bro-cut -h

bro-cut [options] [<columns>]

Extracts the given columns from an ASCII Bro log on standard input.
If no columns are given, all are selected. By default, bro-cut does
not include format header blocks into the output.

Example: cat conn.log | bro-cut -d ts id.orig_h id.orig_p

    -c       Include the first format header block into the output.
    -C       Include all format header blocks into the output.
    -d       Convert time values into human-readable format.
    -D <fmt> Like -d, but specify format for time (see strftime(3) for syntax).
    -F <ofs> Sets a different output field separator.
    -n       Print all fields *except* those specified.
    -u       Like -d, but print timestamps in UTC instead of local time.
    -U <fmt> Like -D, but print timestamps in UTC instead of local time.

For time conversion option -d or -u, the format string can be specified by
setting an environment variable BRO_CUT_TIMEFMT.

```



如查看conn.log的ts时间戳，源host和源port：

```
cat conn.log | bro-cut -d ts id.orig_h id.orig_p
```

查看五元组：

```
bro-cut ts uid id.orig_h id.resp_h proto < conn.log
或
cat conn.log | bro-cut ts uid id.orig_h id.resp_h proto
```







### 配置：

```
Bro installation root directory:$PREFIX
/usr/local/bro
```

#### local.bro

位置：

```
/usr/local/bro/share/bro/site/local.bro
```



### 数据流统计（字段）：

<http://wiki.intra.tophant.com/pages/viewpage.action?pageId=9641129>



### 脚本：

#### 资料：

中文脚本说明：

<http://blog.csdn.net/mhpmii>

官方脚本说明：

<https://www.bro.org/sphinx/scripting/>

官方语法说明：

<https://www.bro.org/sphinx/script-reference/index.html>

在线执行bro脚本：

<http://try.bro.org/>

bro-package-manager

http://bro-package-manager.readthedocs.io/en/stable/quickstart.html

Bro Package Source

https://github.com/bro/packages







#### 涉及仓库：

Sensor 各个配置项（Kafka、supervisor）Sensor 管理器 Bro Scripts

<http://git.tophant.com/joy.sun/sensor-console>

#### 使用脚本：

```
PREFIX/share/bro/site/local.bro这个路径是我们写脚本的入口
1、/usr/local/bro/share/bro/policy路径中新建自己的策略脚本路径：/usr/local/bro/share/bro/policy/mypolicy
2、将自己的脚本cp到该路径
3、在local.bro中添加脚本加载：@load mypolicy/file_extraction
4、在/usr/local/bro/logs/current路径查看脚本执行结果
```





#### 脚本语法：

##### 数据类型：

<http://blog.csdn.net/mhpmii/article/details/52936308>

| Name                       | Description                          |
| -------------------------- | ------------------------------------ |
| bool                       | 布尔类型                                 |
| count, int, double         | 数字类型                                 |
| time, interval             | 时间类型                                 |
| string                     | 字符串                                  |
| pattern                    | 正则表达式                                |
| port, addr, subnet         | 网络类型                                 |
| enum                       | 枚举(用户自定义类型)                          |
| table, set, vector, record | 容器类型                                 |
| function, event, hook      | 可执行类型                                |
| file                       | 文件类型 (only for writing)              |
| opaque                     | 透明类型 (for some built-in functions)   |
| any                        | Any 类型 (for functions or containers) |



##### 类比python类型：

| bro    | python                                   |
| ------ | ---------------------------------------- |
| set    | tuple                                    |
| table  | {[1] = "one", [3] = "three",[5] = "five" } |
| vector | list                                     |
| record | dict                                     |





##### 数据类型详解：

###### pattern

用于文本搜索的正则表达式，通过括号内的斜杠创建 (/) 
正则表达式规则参照[flex 正则表达式](http://flex.sourceforge.net/manual/Patterns.html) 
pattern支持两种匹配，精确匹配(exact)和嵌入匹配(embedded) 
精确匹配使用 “==” 来关联匹配的字符 
例：

```
    /foo|bar/ =="foo";     将返回true
    /foo|bar/ == "foobar"  返回false
```

embedded 匹配使用 “in” 来进行匹配（!in 也支持）

```
    /foo|bar/ in "foobar" ; 返回true
    /^oob/ in "foobar";     返回false
```



###### port

表示传输层的端口号类型 
无符号整型跟上 /tcp./udp,/icmp./unknow中的一个 
不同协议的端口号比较操作是 
unknown < tcp < udp < icmp 
比如 65535/tcp 就小于 0/udp 
可以通过内建函数 *get_port_transport_proto* 来获得传输层协议类型 
或者通过内建函数 *port_to_count* 获得数字类型的端口号



###### addr

表示IP地址的数据类型

```
local a: addr = 192.168.1.100
local s：subnet = 192.168.0.0/16
if(a/16 == s)
    print "true";  
```

检查一个地址是否属于某个 *subnet* ,可以通过in ,!in 来判断

```
local a: addr = 192.168.1.100;
local s: subnet = 192.168.0.0/16;
if(a in s)
    print "true";
```

可以通过内建函数 *is_v4_addr, is_v6_addr* 来检查一个地址是ipv4还是ipv6

另外 hostname 也是可以使用的，但是主机名可能包含多个IP地址，所以这种情况下这个变量其实是 “set[addr]”

```
local a = www.google.com;
```



###### table

类似于map的概念,一个集合映射到另一个集合 
定义table的语法：

```
table [ type^+] of type
```

索引：type^+ 可以指定一个或者多种类型，通过逗号分割，索引不能是pattern，table,set, vector, file,opaque,any 
例：

```
global a: table[count] of string
```

或者可以更复杂一定

```
global a:table[count] of table[addr,port] of string;
```

table a 索引到 另一个table 再索引到一个string

初始化table

```
global t: table[count] of sting = {
    [11] = "eleven",
    [5] = "five",
};
# 通过另一个table初始化
global t2 = table{
    [192.168.0.2,22/tcp] = "ssh",
    [192.168.0.3,80/tcp] = "http"
};
```

table 结构也可以被type命名为一个类型，这可以用在当一个复杂的索引类型双关

```
type MyRec:record {
    a:count &optional;
    b:count;
}

type MyTable: table[MyRec] of strubg;

global t3 = MyTable{[[$b=5]] = "b5",[[$b=7]] = "b7" };
```

获取table 的元素可以通过索引值加”[ ]”的方式

```
print t[11];
```

元素成员可以通过”in” 和 “!in” 来检测

```
if (13 in t)
    ...
if ([192.168.0.2,22/tcp] in t2)
    ...
```

也可以通过索引来重新赋值

```
t[13] = "thirteen";
```

删除table 中的元素可以通过 “delete “关键字

```
delete t[13];
```

如果不存在索引为13的元素，则什么也不会发生

通过取绝对值的操作，可以获得元素的个数

```
|t|
```

这个操作可以用于for 语句中



###### set

和类型 **table** 相似，但是这个集合没有映射关系 
声明语法：

```
set [type^+]
```

通过逗号分割多种类型，有效的类型不包含 *pattern,table,set,vector,file,opaque,any* 
set 可以通过大括号列出元素值来初始化

```
global s: set[port] = {21/tcp,23/tcp};
global s2: set[port,string] = {[21/tcp,"ftp"],[23/tcp,"telnet"]};
```

也可以直接通过另一个set来创建

```
global s3 = set(21/tcp,23/tcp,80/tcp,442/tcp);
```

set 结构也可以被type命名为一个类型，这可以用在当一个复杂的索引类型双关

```
type MyRec: record {
    a: count &optional;
    b: count;
};

type MySet : set[MyRec];

global s4 = MySet([$b=1],[$b=2]);
```

元素成员可以通过 “in” 和 “!in” 来判断

```
if (21/tcp in s)
    ...
if ([21/tcp,"ftp"] !in s2)
    ...
```

通过关键字 **add**来添加set成员

```
add s[22/tcp];
```

如果成员已经存在那么什么也不会发生 
通过关键字 **delete** 来删除一个set成员

```
delete s[21/tcp];
```

如果成员不存在，什么也不会发生；

通过取绝对值的操作，可以获得元素的个数

```
|s|
```

这个操作可以用于for 语句中



###### vector

同样的类似于table,但始终是通过**count**类型来进行索引的且始终是从零开始索引的，声明语句如下

```
global v: vector of string;
```

可以通过vector来行径构造

```
local v = vector("one","two","three");
```

vector 结构也可以被type命名为一个类型，这可以用在当一个复杂的索引类型双关

```
type MyRec : record {
    a:count &optional;
    b:count;
};

type MyVec :vector of MyRec;

global v2 = myVec([$b=1],[$b=2],[$b=3]);
```

通过索引来和”[ ]”来获取元素

```
print v[2];
```

通过索引来直接赋值	

```
v[3] = "four";
```

通过取绝对值的操作，可以获得元素的个数

```
|v|
```

如果vectors的数据是整数（int 或 count）,则支持直接进行“++” ， “–”才操作； 
如果是数字型（int ,count ,double）,则可以支持“+”，“-”,”*”,”/”，“%”的操作 
但是这些操作需要有相同的元素个数 
如果是布尔型(bool),则可以直接进行“&&”，“||”的操作



###### reocrd

record类型是数据的集合，所有的数据都具有名称和值两个域，他们不需要具有相同的数据类型，类型也没有限制（有点像结构体），例：

```
type MyRecordType:record {
    c:count;
    s:string &optional;
};
```

records 类型可以通过三种方式进行初始化或者赋值，所有没有 *&optinal *或者 *&default*属性的元素必须被明确赋值，例：

```
local r:MyRecordType = record($c = 7);
```

因为record类型一般通过type定义,所以可以使用更可读的方式进行声明和赋值

```
local r = MyRecordType($c = 42);
```

第三种方式像这样:

```
local r:MyRecordType = [$c = 13,$s="thirteen"];
```

获取元素域通过 “$” 符号来操作，如下

```
local r: MyRecordType;
r$c = 12;
```

测试具有 “&optional “属性的域是否被赋值，可以通过*？$* 操作符返回一个bool类型来进行判断（T:有，F:没有）

```
if (r ?$ s)
    ...
```



###### function

在bro 中，function 类型通过如下方法声明：

```
function(argument *): type
```

参数(argument )可以为空或者是通过逗号来分割，返回值（type） 是可选的，例子：

```
global greeting :function(name: string):string;
```

这里 *greeting* 是函数的标识，函数体还未定义，函数的函数体甚至可以在不同的时间有不同的函数体，定义一个包含函数体的函数：

```
function greeting(name: string):string
    {
    return "Heloow," + name;
    }
```

通过这种方式定义函数，就不需要像上面那样对函数进行声明，如果要声明的话，那函数类型返回值，参数列表必须完全一致

定义一个没有参数没有返回值的函数：

```
function my_func()
    {
    print "my_func";
    }
```

赋值一个匿名函数

```
greeting = function(name:string):string {return "Hi, "+ name};
```

调用函数：

```
print greeting("Dave");
```

默认参数的参数放在参数列表的最后：

```
global foo:function(s: string,t :string &default="abc",u: count &default =0);
```

如果一个函数之前被声明为使用默认参数，当定义函数体的时候这些默认参数可以不写，在调用的时候任然有效

```
function foo(s: string,t:string.u:count)
    {
    print s,t,u;
    }
```

调用该函数可以省略从参数列表中的默认值：

```
 foo("test");
```



###### hook

Hook 是另一种具备 function 和 evnet 特点的 “function” 
具有相同标识符的 hook 可以通过*&priority* 属性来按照优先级执行，调用的时候他们更像是function,因为和envent不同，他们不能通过scheduled 放入event队列而是被立即执行，同时，hook的一个独有特点是hook的handler 函数体可以通过”break ” 关键字让剩余的处理程序的语句中断，（return 是在函数体结束的时候退出）

hook的声明方式

```
hook (argument *)
```

argument 可以为空或者是逗号分割的列表，例子

```
global myhook: hook(s:string)
```

这里只是定义了hook的标识，没有handler body,我们可以定义多个handler bodies:

```
hook myhook(s:string) &porority=10
    {
    print "porority 10 myhook handler",s;
    s = "bye";
    }
hook myhook(s:string)
    {
    print "break out of myhook handling ",s;
    }
hook myhook(s: string) &porority=-5
    {
    print "not going to happend",s;
    }
```

要立即执行 hook 处理，调用方式和function 类似，只不过要通过hook 关键字来调用：

```
 hook myhook("hi");
```

或者

```
if(hook myhook("hi"))
    print "all handlers ran";
```

输出如下：

```
priority 10 myhook handler,hi
break out of myhook handling ,bye
```

注意到参数可以被先执行的hook 修改

hook 执行的返回值是 bool型的（T or F）,T 说明所有的hook都被执行了，F指示只有部分hook被执行了，一般F是break 语句执行的结果







##### 属性：

**Bro 脚本语言支持下面这些属性**

| 名称               | 描述                                       |
| ---------------- | ---------------------------------------- |
| &redef           | 重新定义一个全局的常量或者扩展一种类型.                     |
| &priority        | 指示event 或者hook的优先级.                      |
| &log             | 标记record中的字段写入日志.                        |
| &optional        | 允许字段为空                                   |
| &default         | 指定默认参数.                                  |
| &add_func        | 为每个 “redef +=”指定调用函数.                    |
| &delete_func     | 和 “&add_func”一样, 只不过是为 “redef -=”指定.     |
| &expire_func     | 为“container element expires”指定调用函数.      |
| &read_expire     | 指定读超时间隔.                                 |
| &write_expire    | 指定写超时间隔.                                 |
| &create_expire   | 指定创建的超时间隔.                               |
| &synchronized    | Synchronize a variable across nodes.     |
| &persistent      | Make a variable persistent (written to disk). |
| &rotate_interval | 轮询（Rotate)文件时间间隔.                        |
| &rotate_size     | 轮询（Rotate）文件大小.                          |
| &encrypt         | 写文件的时候加密.                                |
| &raw_output      | 以原始模式打开文件 (chars. are not escaped).      |
| &mergeable       | Prefer set union for synchronized state. |
| &error_handler   | Used internally for reporter framework events. |
| &type_column     | Used by input framework for “port” type. |
| &deprecated      | Marks an identifier as deprecat.         |



##### 属性详解：





##### 声明和语句：

###### Declarations

| Name                | Description              |
| ------------------- | ------------------------ |
| module              | 改变当前模块                   |
| export              | 从当前模块导出定义                |
| global              | 声明一个全局变量                 |
| const               | 声明一个全局常量                 |
| type                | 声明一个一用户自定义类型             |
| redef               | 重新定义一个全局值或者扩展一个用户自定义类型   |
| function/event/hook | 声明一个 function/event/hook |

###### Statements

| Name                       | Description                     |
| -------------------------- | ------------------------------- |
| local                      | 声明一个局部变量                        |
| add, delete                | 添加或删除元素                         |
| print                      | 打印到标准输出或文件                      |
| for, while, next, break    | 遍历所有容器的元素(for), 条件循环(while).    |
| if                         | 表达式bool条件判断执行                   |
| switch, break, fallthrough | 计算表达式和匹配值执行语句                   |
| when                       | 异步执行                            |
| event, schedule            | 调用或调度的事件处理程序                    |
| return                     | 从 function, hook, 或event 处理程序返回 |



##### 声明详解



###### **module**

关键字module 用于改变当前的module,这会影响任何随后全局标识符作用范围 
例子：

```
module mymodule1
```

如果一个全局的定义（global）声明在module的后面，那他的作用域在Bro脚本结束的地方或者在下一个module声明的位置，如果一个全局的声明在module的后面，但是在export 语句块中，那么它的作用域将扩展到最后一个load的bro脚本结束，但是在其他的module中它必须通过命名空间操作符（::）来进行引用 
在一个bro脚本中，可以有多个module声明，同一个module也可以写在多个不同的bro脚本中



###### **export** 

export 语句块将当前module中的一个或者多个声明（不能将语句块写在其中）导出，在其他module中，这些全局标识通过操作符”(::)”变得可见 
例子：

```
export {
    redef enum Log::ID += {LOG};

    type Info: record {
        ts: time &log;
        uid: sting &log;
    };

    const conntime = 30sec &redef;

}
```

> 注意，在导出块中括号是必须的，而且这个语句块也不需要用分号结束



###### type 

type 关键字用于声明一个用户自定义的类型，新的类型将拥有全局的作用域，也可以用在任何内建类型出现的地方 
type 关键字通常被用于定义 record 或者 enum , 当然在处理复杂类型的时候也很有用 
例子：

```
type mytype:table[count] of table[addr,port] of string;
global myvar: mytype;
```



###### **redef** 

有三种方式来使用redef　：　 
用于改变全局变量的值(含有&redef 属性的变量) 
用来扩展 record 类型或者 enum 类型 
用来明确指定一个新的event处理函数替代之前所有的处理函数

如果你使用 “redef” 来改变一个全局变量（global 或者 const ）,那么这个变量需要有&redef 属性，如果要修改的变量是 table,set,或者是pattern,就必须使用 **+=**操作符来添加新成员，否则直接用=号的话将会分配一个新的值，如果操作的对象是 table 或者set，可以使用**-=**操作符来移除已有的元素，其他情况下，你要通过**=**号来重新赋值，例：

```
redef pi = 3.14;
```

如果你用redef 来扩展 record 或者 enum，那么你必须使用 **+=**操作符，对于enum来说，你可以添加更多的枚举常量，对于record ，你可以添加更多的record字段，这时候，通过redef添加的字段，必须含有 &optional 或者 &default 属性，例：

```
redef enum color += {Blue,Red};
redef record MyRecord += {n2:int &optional;s2:string &optional;};
```

如果你使用redef 来替换event的处理函数，之前的函数将被完全移除（这个语句后的子event处理函数不会受到影响），语法和常规的event 处理函数的定义完全一样除了前面加了 ”redef“:

```
redef event myevent(s:string) {print "Redefined",s;}
```



##### 语句详解

###### **local** 

声明一个本地变量，可以通过初始化值自动推断类型，否则要明确指定类型

```
local x1 = 5.7;
local x2:double ;
local x3:double = 5.3;123
```

hook,event,function 处理函数中，要求使用local 关键字来声明变量（除了const 声明和 for 语句中的隐式声明） 
local 变量的作用域就仅限于声明的function,event,hook 处理函数中



##### 事件

###### 系统自带事件:

<https://www.bro.org/sphinx/scripts/base/bif/event.bif.bro.html>

###### connection相关事件：

<https://www.bro.org/sphinx/scripts/base/bif/event.bif.bro.html#id-new_connection>

###### 文件传输事件：

<https://www.bro.org/sphinx/scripts/base/bif/event.bif.bro.html?highlight=file_over_new_connection#id-file_over_new_connection>





##### 统计功能SumStats

<http://try.bro.org/#/trybro/saved/200173>

<https://www.bro.org/sphinx/scripts/base/frameworks/sumstats/main.bro.html#type-SumStats::Calculation>

```perl
@load base/frameworks/sumstats
event bro_init()
    {
    local r1 = SumStats::Reducer($stream="dns.lookup", $apply=set(SumStats::UNIQUE));
    SumStats::create([$name="dns.requests.unique",
                      $epoch=6hrs,
                      $reducers=set(r1),
                      $epoch_result(ts: time, key: SumStats::Key, result: SumStats::Result) =
                        {
                        local r = result["dns.lookup"];
                        print fmt("%s did %d total and %d unique DNS requests in the last 6 hours.", 
                        			key$host, r$num, r$unique);
                        }]);
    }

event dns_request(c: connection, msg: dns_msg, query: string, qtype: count, qclass: count)
    {
    if ( c$id$resp_p == 53/udp && query != "" ) # to limit this to port 53, non-empty requests and only local hosts
        SumStats::observe("dns.lookup", [$host=c$id$orig_h], [$str=query]);
    }

```



#### 脚本案例：

##### 官方脚本

`https://www.bro.org/sphinx/script-reference/scripts.html`



##### 内部与外部连接：

```perl
global local_subnets: set[subnet] = { 192.168.1.0/24, 192.68.2.0/24, 172.16.0.0/20, 172.16.16.0/20, 172.16.32.0/20, 172.16.48.0/20 };
global my_count = 0;
global inside_networks: set[addr];
global outside_networks: set[addr];

event new_connection(c: connection)
    {
    ++my_count;
    if ( my_count <= 10 )
	{
        print fmt("The connection %s from %s on port %s to %s on port %s started at %s.", c$uid, c$id$orig_h, c$id$orig_p, c$id$resp_h, c$id$resp_p, strftime("%D %H:%M", c$start_time)); 
    }
    if ( c$id$orig_h in local_subnets)
    	{
	add inside_networks[c$id$orig_h];
        }
    else
        add outside_networks[c$id$orig_h];
	    
    if ( c$id$resp_h in local_subnets)
        {
        add inside_networks[c$id$resp_h];
        }
    else
        add outside_networks[c$id$resp_h];
    }

event connection_state_remove(c: connection)
    {
    if ( my_count <= 10 )
    	{
    	print fmt("Connection %s took %s seconds", c$uid, c$duration);	
    	}
    }

event bro_done() 
    {
    print fmt("Saw %d new connections", my_count);
    print "These IPs are considered local";
    for (a in inside_networks)
        {
        print a;
        }
    print "These IPs are considered external";
    for (a in outside_networks)
        {
        print a;
        }
    }

```



##### 日志流：

<http://try.bro.org/#/?example=modules-log-factorial>

factorial.bro

```perl
module Factor;

export {
    # Append the value LOG to the Log::ID enumerable.
    redef enum Log::ID += { LOG };

    # Define a new type called Factor::Info.
    type Info: record {
        num:           count &log;
        factorial_num: count &log;
        };
    global factorial: function(n: count): count;
    }
    
function factorial(n: count): count
    {
    if ( n == 0 )
        return 1;
    
    else
        return ( n * factorial(n - 1) );
    }

```

main.bro

```perl
@load factorial

event bro_init()
    {
    # Create the logging stream.
    Log::create_stream(Factor::LOG, [$columns=Factor::Info, $path="factor"]);
    }

event bro_done()
    {
    local numbers: vector of count = vector(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);    
    for ( n in numbers )
        Log::write( Factor::LOG, [$num=numbers[n],
                                  $factorial_num=Factor::factorial(numbers[n])]);
    }

```



##### 日志切割Filtering Logs：

<http://try.bro.org/#/trybro/saved/200162>

main.bro

```perl
@load factorial

event bro_init()
    {
    Log::create_stream(Factor::LOG, [$columns=Factor::Info, $path="factor"]);
    
    local filter: Log::Filter = [$name="split-mod5s", $path_func=Factor::mod5];
    Log::add_filter(Factor::LOG, filter);
    Log::remove_filter(Factor::LOG, "default");
    }

event bro_done()
    {
    local numbers: vector of count = vector(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);    
    for ( n in numbers )
        Log::write( Factor::LOG, [$num=numbers[n],
                                  $factorial_num=Factor::factorial(numbers[n])]);
    }

```

fatorial.bro

```perl
module Factor;

export {
    # Append the value LOG to the Log::ID enumerable.
    redef enum Log::ID += { LOG };

    # Define a new type called Factor::Info.
    type Info: record {
        num:           count &log;
        factorial_num: count &log;
        };
    global factorial: function(n: count): count;
    global mod5: function(id: Log::ID, path: string, rec: Factor::Info) : string;
    }
    
function factorial(n: count): count
    {
    if ( n == 0 )
        return 1;
    
    else
        return ( n * factorial(n - 1) );
    }
    
function mod5(id: Log::ID, path: string, rec: Factor::Info) : string    
    {
    if ( rec$factorial_num % 5 == 0 )
        return "factor-mod5";
    
    else
        return "factor-non5";
    }

```







##### 文件传输

http://wiki.intra.tophant.com/pages/viewpage.action?pageId=9641267

```bash
module Test4FAF;
@load policy/misc/capture-loss.bro
@load base/files/extract/main.bro
export {
        const path: string = "/root/myth/bro-files-test/files" &redef;
        redef FileExtract::default_limit: count = 10485760;
        redef default_file_bof_buffer_size: count = 4096;
}
event bro_init() &priority=-5
{
    print "bro start ...";
}
 
event file_sniff(f: fa_file, meta: fa_metadata)
{
    # check http request uri to make sure file extraction is just for out test file
    if ( f?$http && f$http?$uri && /test-for-bro-[0-9]+k\.(html|dat)/ in f$http$uri ){
        local fname = fmt("%s%s_%s", path, f$http$uri , f$id);
        Files::add_analyzer(f, Files::ANALYZER_EXTRACT,[$extract_filename=fname]);
    }
}

```



##### detect_MHR.bro

```shell
##! Detect file downloads that have hash values matching files in Team
##! Cymru's Malware Hash Registry (http://www.team-cymru.org/Services/MHR/).

##### 函数库
@load base/frameworks/files
@load base/frameworks/notice
@load frameworks/files/hash-all-files

module TeamCymruMalwareHashRegistry;  # namespace

#######
export {
	redef enum Notice::Type += {
		## The hash value of a file transferred over HTTP matched in the
		## malware hash registry.
		Match
	};

	## File types to attempt matching against the Malware Hash Registry.
	const match_file_types = /application\/x-dosexec/ |
	                         /application\/vnd.ms-cab-compressed/ |
	                         /application\/pdf/ |
	                         /application\/x-shockwave-flash/ |
	                         /application\/x-java-applet/ |
	                         /application\/jar/ |
	                         /video\/mp4/ &redef;

	## The Match notice has a sub message with a URL where you can get more
	## information about the file. The %s will be replaced with the SHA-1
	## hash of the file.
	const match_sub_url = "https://www.virustotal.com/en/search/?query=%s" &redef;

	## The malware hash registry runs each malware sample through several
	## A/V engines.  Team Cymru returns a percentage to indicate how
	## many A/V engines flagged the sample as malicious. This threshold
	## allows you to require a minimum detection rate.
	const notice_threshold = 10 &redef;
}
######
function do_mhr_lookup(hash: string, fi: Notice::FileInfo)
	{
	local hash_domain = fmt("%s.malware.hash.cymru.com", hash);

	when ( local MHR_result = lookup_hostname_txt(hash_domain) )
		{
		# Data is returned as "<dateFirstDetected> <detectionRate>"
		local MHR_answer = split_string1(MHR_result, / /);

		if ( |MHR_answer| == 2 )
			{
			local mhr_detect_rate = to_count(MHR_answer[1]);

			if ( mhr_detect_rate >= notice_threshold )
				{
				local mhr_first_detected = double_to_time(to_double(MHR_answer[0]));
				local readable_first_detected = strftime("%Y-%m-%d %H:%M:%S", mhr_first_detected);
				local message = fmt("Malware Hash Registry Detection rate: %d%%  Last seen: %s", mhr_detect_rate, readable_first_detected);
				local virustotal_url = fmt(match_sub_url, hash);
				# We don't have the full fa_file record here in order to
				# avoid the "when" statement cloning it (expensive!).
				local n: Notice::Info = Notice::Info($note=Match, $msg=message, $sub=virustotal_url);
				Notice::populate_file_info2(fi, n);
				NOTICE(n);
				}
			}
		}
	}
######
event file_hash(f: fa_file, kind: string, hash: string)
	{
	if ( kind == "sha1" && f?$info && f$info?$mime_type && 
	     match_file_types in f$info$mime_type )
		do_mhr_lookup(hash, Notice::create_file_info(f));
	}

```



##### 捕捉HTTP流量

参考：

`http://blog.csdn.net/mhpmii/article/details/52936378`



```bash
@load base/utils/site
@load base/frameworks/notice

redef Site::local_nets += { 192.168.0.0/16 };

module HTTP;

export {

    redef enum Notice::Type += {
        Open_Proxy
    };

    global success_status_codes: set[count] = {
        200,
        201,
        202,
        203,
        204,
        205,
        206,
        207,
        208,
        226,
        304
    };
}

event http_reply(c: connection, version: string, code: count, reason: string)
    {
    if ( Site::is_local_addr(c$id$resp_h) &&
         /^[hH][tT][tT][pP]:/ in c$http$uri &&
         c$http$status_code in HTTP::success_status_codes )
        NOTICE([$note=HTTP::Open_Proxy,
                $msg=fmt("A local server is acting as an open proxy: %s",
                         c$id$resp_h),
                $conn=c,
                $identifier=cat(c$id$resp_h),
                $suppress_for=1day]);
    }
```



##### detect-sqli.bro

```bash
##! SQL injection attack detection in HTTP.

@load base/frameworks/notice
@load base/frameworks/sumstats
@load base/protocols/http

module HTTP;

export {
	redef enum Notice::Type += {
		## Indicates that a host performing SQL injection attacks was
		## detected.
		SQL_Injection_Attacker,
		## Indicates that a host was seen to have SQL injection attacks
		## against it.  This is tracked by IP address as opposed to
		## hostname.
		SQL_Injection_Victim,
	};

	redef enum Tags += {
		## Indicator of a URI based SQL injection attack.
		URI_SQLI,
		## Indicator of client body based SQL injection attack.  This is
		## typically the body content of a POST request. Not implemented
		## yet.
		POST_SQLI,
		## Indicator of a cookie based SQL injection attack. Not
		## implemented yet.
		COOKIE_SQLI,
	};

	## Defines the threshold that determines if an SQL injection attack
	## is ongoing based on the number of requests that appear to be SQL
	## injection attacks.
	const sqli_requests_threshold: double = 50.0 &redef;

	## Interval at which to watch for the
	## :bro:id:`HTTP::sqli_requests_threshold` variable to be crossed.
	## At the end of each interval the counter is reset.
	const sqli_requests_interval = 5min &redef;

	## Collecting samples will add extra data to notice emails
	## by collecting some sample SQL injection url paths.  Disable
	## sample collection by setting this value to 0.
	const collect_SQLi_samples = 5 &redef;

	## Regular expression is used to match URI based SQL injections.
	const match_sql_injection_uri =
		  /[\?&][^[:blank:]\x00-\x37\|]+?=[\-[:alnum:]%]+([[:blank:]\x00-\x37]|\/\*.*?\*\/)*['"]?([[:blank:]\x00-\x37]|\/\*.*?\*\/|\)?;)+.*?([hH][aA][vV][iI][nN][gG]|[uU][nN][iI][oO][nN]|[eE][xX][eE][cC]|[sS][eE][lL][eE][cC][tT]|[dD][eE][lL][eE][tT][eE]|[dD][rR][oO][pP]|[dD][eE][cC][lL][aA][rR][eE]|[cC][rR][eE][aA][tT][eE]|[iI][nN][sS][eE][rR][tT])([[:blank:]\x00-\x37]|\/\*.*?\*\/)+/
		| /[\?&][^[:blank:]\x00-\x37\|]+?=[\-0-9%]+([[:blank:]\x00-\x37]|\/\*.*?\*\/)*['"]?([[:blank:]\x00-\x37]|\/\*.*?\*\/|\)?;)+([xX]?[oO][rR]|[nN]?[aA][nN][dD])([[:blank:]\x00-\x37]|\/\*.*?\*\/)+['"]?(([^a-zA-Z&]+)?=|[eE][xX][iI][sS][tT][sS])/
		| /[\?&][^[:blank:]\x00-\x37]+?=[\-0-9%]*([[:blank:]\x00-\x37]|\/\*.*?\*\/)*['"]([[:blank:]\x00-\x37]|\/\*.*?\*\/)*(-|=|\+|\|\|)([[:blank:]\x00-\x37]|\/\*.*?\*\/)*([0-9]|\(?[cC][oO][nN][vV][eE][rR][tT]|[cC][aA][sS][tT])/
		| /[\?&][^[:blank:]\x00-\x37\|]+?=([[:blank:]\x00-\x37]|\/\*.*?\*\/)*['"]([[:blank:]\x00-\x37]|\/\*.*?\*\/|;)*([xX]?[oO][rR]|[nN]?[aA][nN][dD]|[hH][aA][vV][iI][nN][gG]|[uU][nN][iI][oO][nN]|[eE][xX][eE][cC]|[sS][eE][lL][eE][cC][tT]|[dD][eE][lL][eE][tT][eE]|[dD][rR][oO][pP]|[dD][eE][cC][lL][aA][rR][eE]|[cC][rR][eE][aA][tT][eE]|[rR][eE][gG][eE][xX][pP]|[iI][nN][sS][eE][rR][tT])([[:blank:]\x00-\x37]|\/\*.*?\*\/|[\[(])+[a-zA-Z&]{2,}/
		| /[\?&][^[:blank:]\x00-\x37]+?=[^\.]*?([cC][hH][aA][rR]|[aA][sS][cC][iI][iI]|[sS][uU][bB][sS][tT][rR][iI][nN][gG]|[tT][rR][uU][nN][cC][aA][tT][eE]|[vV][eE][rR][sS][iI][oO][nN]|[lL][eE][nN][gG][tT][hH])\(/
		| /\/\*![[:digit:]]{5}.*?\*\// &redef;
}

function format_sqli_samples(samples: vector of SumStats::Observation): string
	{
	local ret = "SQL Injection samples\n---------------------";
	for ( i in samples )
		ret += "\n" + samples[i]$str;
	return ret;
	}

event bro_init() &priority=3
	{
	# Add filters to the metrics so that the metrics framework knows how to
	# determine when it looks like an actual attack and how to respond when
	# thresholds are crossed.
	local r1: SumStats::Reducer = [$stream="http.sqli.attacker", $apply=set(SumStats::SUM, SumStats::SAMPLE), $num_samples=collect_SQLi_samples];
	SumStats::create([$name="detect-sqli-attackers",
	                  $epoch=sqli_requests_interval,
	                  $reducers=set(r1),
	                  $threshold_val(key: SumStats::Key, result: SumStats::Result) =
	                  	{
	                  	return result["http.sqli.attacker"]$sum;
	                  	},
	                  $threshold=sqli_requests_threshold,
	                  $threshold_crossed(key: SumStats::Key, result: SumStats::Result) =
	                  	{
	                  	local r = result["http.sqli.attacker"];
	                  	NOTICE([$note=SQL_Injection_Attacker,
	                  	        $msg="An SQL injection attacker was discovered!",
	                  	        $email_body_sections=vector(format_sqli_samples(r$samples)),
	                  	        $src=key$host,
	                  	        $identifier=cat(key$host)]);
	                  	}]);

	local r2: SumStats::Reducer = [$stream="http.sqli.victim", $apply=set(SumStats::SUM, SumStats::SAMPLE), $num_samples=collect_SQLi_samples];
	SumStats::create([$name="detect-sqli-victims",
	                  $epoch=sqli_requests_interval,
	                  $reducers=set(r2),
	                  $threshold_val(key: SumStats::Key, result: SumStats::Result) =
	                  	{
	                  	return result["http.sqli.victim"]$sum;
	                  	},
	                  $threshold=sqli_requests_threshold,
	                  $threshold_crossed(key: SumStats::Key, result: SumStats::Result) =
	                  	{
	                  	local r = result["http.sqli.victim"];
	                  	NOTICE([$note=SQL_Injection_Victim,
	                  	        $msg="An SQL injection victim was discovered!",
	                  	        $email_body_sections=vector(format_sqli_samples(r$samples)),
	                  	        $src=key$host,
	                  	        $identifier=cat(key$host)]);
	                  	}]);
	}

event http_request(c: connection, method: string, original_URI: string,
                   unescaped_URI: string, version: string) &priority=3
	{
	if ( match_sql_injection_uri in unescaped_URI )
		{
		add c$http$tags[URI_SQLI];

		SumStats::observe("http.sqli.attacker", [$host=c$id$orig_h], [$str=original_URI]);
		SumStats::observe("http.sqli.victim",   [$host=c$id$resp_h], [$str=original_URI]);
		}
	}

```



##### tophant.entrypoint.bro

```perl
@load policy/tuning/json-logs
@load Bro/Kafka/logs-to-kafka

module Tophant;

export{
    global DEBUG: bool = F;
    function debug(msg: string){
        if(Tophant::DEBUG){
            print fmt("[DEBUG] %s - %s", strftime("%Y-%m-%d %H:%M:%S", current_time()), msg);
        }
    }
    global my_ip: string = "";
}

#################################### 加载功能脚本
# 新资产相关的脚本
@load ./tophant.asset.bro
# 总带宽、http带宽、总处理包、丢包等数据的统计脚本
#@load ./tophant.stats.bro
# 提供 PVS 分析引擎所需数据
@load ./tophant.pvs.bro
# bro 运行性能统计测试脚本
#@load ./tophant.profile.bro

@load ./tophant.file.bro
@load ./tophant.software.bro

@load ./tophant.ftp.bro
@load ./tophant.arp.bro
@load ./tophant.dns.bro
@load ./tophant.icmp.bro
@load ./tophant.mysql.bro
@load ./tophant.pop3.bro
@load ./tophant.rdp.bro
@load ./tophant.smtp.bro
@load ./tophant.tcp.bro
@load ./tophant.udp.bro
@load ./tophant.ssh.bro
@load ./tophant.ssl.bro
@load ./tophant.socks.bro
@load ./tophant.tunnels.bro
@load ./tophant.snmp.bro
@load ./tophant.telnet.bro
@load ./tophant.dhcp.bro
@load ./tophant.ntp.bro
#@load ./tophant.weird.bro
@load ./tophant.smb.bro
@load ./tophant.ntlm.bro

redef Kafka::kafka_conf = table(
    ["metadata.broker.list"] = "127.0.0.1:9091"
);

event bro_init() &priority=-5
{
    when (local output = Exec::run([$cmd="ifconfig | grep -A 1 eno2 | tail -n 1 | awk '{print $2}'"])){
        if ( output$exit_code == 0 && |output$stdout| > 0){
            Tophant::my_ip = output$stdout[0];
            Tophant::debug(fmt("get my ip is %s", Tophant::my_ip));
        }
    }
    # remove default writer for every log stream
    for(log_id in Log::active_streams){
            if(! Tophant::DEBUG){
                print fmt("remove default filter for log id : %s", log_id);
                Log::remove_default_filter(log_id);
        }
    }
}

```



`$cmd="ifconfig | grep -A 1 eno2 | tail -n 1 | awk '{print $2}'"`这句运行后获得当前主机eno2网卡ip地址





##### detect-bruteforcing.bro

分析文档位于：

<https://www.bro.org/sphinx/broids/index.html#detecting-an-ftp-brute-force-attack-and-notifying>

```perl
##! FTP brute-forcing detector, triggering when too many rejected usernames or
##! failed passwords have occurred from a single address.

@load base/protocols/ftp
@load base/frameworks/sumstats

@load base/utils/time

module FTP;

export {
	redef enum Notice::Type += {
		## Indicates a host bruteforcing FTP logins by watching for too
		## many rejected usernames or failed passwords.
		Bruteforcing
	};

	## How many rejected usernames or passwords are required before being
	## considered to be bruteforcing.
	const bruteforce_threshold: double = 20 &redef;

	## The time period in which the threshold needs to be crossed before
	## being reset.
	const bruteforce_measurement_interval = 15mins &redef;
}


event bro_init()
	{
	local r1: SumStats::Reducer = [$stream="ftp.failed_auth", $apply=set(SumStats::UNIQUE), $unique_max=double_to_count(bruteforce_threshold+2)];
	SumStats::create([$name="ftp-detect-bruteforcing",
	                  $epoch=bruteforce_measurement_interval,
	                  $reducers=set(r1),
	                  $threshold_val(key: SumStats::Key, result: SumStats::Result) =
	                  	{
	                  	return result["ftp.failed_auth"]$num+0.0;
	                  	},
	                  $threshold=bruteforce_threshold,
	                  $threshold_crossed(key: SumStats::Key, result: SumStats::Result) =
	                  	{
	                  	local r = result["ftp.failed_auth"];
	                  	local dur = duration_to_mins_secs(r$end-r$begin);
	                  	local plural = r$unique>1 ? "s" : "";
	                  	local message = fmt("%s had %d failed logins on %d FTP server%s in %s", key$host, r$num, r$unique, plural, dur);
	                  	NOTICE([$note=FTP::Bruteforcing,
	                  	        $src=key$host,
	                  	        $msg=message,
	                  	        $identifier=cat(key$host)]);
	                  	}]);
	}

event ftp_reply(c: connection, code: count, msg: string, cont_resp: bool)
	{
	local cmd = c$ftp$cmdarg$cmd;
	if ( cmd == "USER" || cmd == "PASS" )
		{
		if ( FTP::parse_ftp_reply_code(code)$x == 5 )
			SumStats::observe("ftp.failed_auth", [$host=c$id$orig_h], [$str=cat(c$id$resp_h)]);
		}
	}

```











### 文件目录结构：


```
.
├── ./bin
│   ├── ./bin/bro
│   ├── ./bin/broccoli-config
│   ├── ./bin/bro-config
│   ├── ./bin/broctl
│   ├── ./bin/bro-cut
│   ├── ./bin/capstats
│   └── ./bin/trace-summary
├── ./etc
│   ├── ./etc/broccoli.conf
│   ├── ./etc/broctl.cfg  # 日志归案设置
│   ├── ./etc/networks.cfg
│   └── ./etc/node.cfg  # 端口
├── ./include
│   └── ./include/broccoli.h
├── ./lib
│   ├── ./lib/bro
│   │   └── ./lib/bro/plugins
│   ├── ./lib/broctl
│   │   ├── ./lib/broctl/broccoli_intern.py
│   │   ├── ./lib/broctl/broccoli_intern.pyc
│   │   ├── ./lib/broctl/_broccoli_intern.so
│   │   ├── ./lib/broctl/broccoli.py
│   │   ├── ./lib/broctl/broccoli.pyc
│   │   ├── ./lib/broctl/BroControl
│   │   │   ├── ./lib/broctl/BroControl/brocmd.py
│   │   │   ├── ./lib/broctl/BroControl/brocmd.pyc
│   │   │   ├── ./lib/broctl/BroControl/broctl.py
│   │   │   ├── ./lib/broctl/BroControl/broctl.pyc
│   │   │   ├── ./lib/broctl/BroControl/cmdresult.py
│   │   │   ├── ./lib/broctl/BroControl/cmdresult.pyc
│   │   │   ├── ./lib/broctl/BroControl/config.py
│   │   │   ├── ./lib/broctl/BroControl/config.pyc
│   │   │   ├── ./lib/broctl/BroControl/control.py
│   │   │   ├── ./lib/broctl/BroControl/control.pyc
│   │   │   ├── ./lib/broctl/BroControl/cron.py
│   │   │   ├── ./lib/broctl/BroControl/cron.pyc
│   │   │   ├── ./lib/broctl/BroControl/doc.py
│   │   │   ├── ./lib/broctl/BroControl/doc.pyc
│   │   │   ├── ./lib/broctl/BroControl/events.py
│   │   │   ├── ./lib/broctl/BroControl/events.pyc
│   │   │   ├── ./lib/broctl/BroControl/exceptions.py
│   │   │   ├── ./lib/broctl/BroControl/exceptions.pyc
│   │   │   ├── ./lib/broctl/BroControl/execute.py
│   │   │   ├── ./lib/broctl/BroControl/execute.pyc
│   │   │   ├── ./lib/broctl/BroControl/__init__.py
│   │   │   ├── ./lib/broctl/BroControl/__init__.pyc
│   │   │   ├── ./lib/broctl/BroControl/install.py
│   │   │   ├── ./lib/broctl/BroControl/install.pyc
│   │   │   ├── ./lib/broctl/BroControl/lock.py
│   │   │   ├── ./lib/broctl/BroControl/lock.pyc
│   │   │   ├── ./lib/broctl/BroControl/node.py
│   │   │   ├── ./lib/broctl/BroControl/node.pyc
│   │   │   ├── ./lib/broctl/BroControl/options.py
│   │   │   ├── ./lib/broctl/BroControl/options.pyc
│   │   │   ├── ./lib/broctl/BroControl/plugin.py
│   │   │   ├── ./lib/broctl/BroControl/plugin.pyc
│   │   │   ├── ./lib/broctl/BroControl/pluginreg.py
│   │   │   ├── ./lib/broctl/BroControl/pluginreg.pyc
│   │   │   ├── ./lib/broctl/BroControl/printdoc.py
│   │   │   ├── ./lib/broctl/BroControl/py3bro.py
│   │   │   ├── ./lib/broctl/BroControl/py3bro.pyc
│   │   │   ├── ./lib/broctl/BroControl/ssh_runner.py
│   │   │   ├── ./lib/broctl/BroControl/ssh_runner.pyc
│   │   │   ├── ./lib/broctl/BroControl/state.py
│   │   │   ├── ./lib/broctl/BroControl/state.pyc
│   │   │   ├── ./lib/broctl/BroControl/utilcurses.py
│   │   │   ├── ./lib/broctl/BroControl/utilcurses.pyc
│   │   │   ├── ./lib/broctl/BroControl/util.py
│   │   │   ├── ./lib/broctl/BroControl/util.pyc
│   │   │   ├── ./lib/broctl/BroControl/version.py
│   │   │   └── ./lib/broctl/BroControl/version.pyc
│   │   ├── ./lib/broctl/plugins
│   │   │   ├── ./lib/broctl/plugins/lb_custom.py
│   │   │   ├── ./lib/broctl/plugins/lb_custom.pyc
│   │   │   ├── ./lib/broctl/plugins/lb_myricom.py
│   │   │   ├── ./lib/broctl/plugins/lb_myricom.pyc
│   │   │   ├── ./lib/broctl/plugins/lb_pf_ring.py
│   │   │   ├── ./lib/broctl/plugins/lb_pf_ring.pyc
│   │   │   ├── ./lib/broctl/plugins/ps.py
│   │   │   ├── ./lib/broctl/plugins/ps.pyc
│   │   │   ├── ./lib/broctl/plugins/TestPlugin.py
│   │   │   └── ./lib/broctl/plugins/TestPlugin.pyc
│   │   ├── ./lib/broctl/SubnetTree.py
│   │   └── ./lib/broctl/_SubnetTree.so
│   ├── ./lib/libbroccoli.a
│   ├── ./lib/libbroccoli.so -> libbroccoli.so.5
│   ├── ./lib/libbroccoli.so.5 -> libbroccoli.so.5.1.0
│   └── ./lib/libbroccoli.so.5.1.0
├── ./logs  # 日志
│   ├── ./logs/2018-01-08
│   │   ├── ./logs/2018-01-08/stderr.18:37:44-20:28:51.log.gz
│   │   └── ./logs/2018-01-08/stdout.18:37:44-20:28:51.log.gz
│   └── ./logs/current -> /usr/local/bro/spool/bro
├── ./share
│   ├── ./share/bro  # 默认使用的脚本
│   │   ├── ./share/bro/base  # 自动加载的脚本
│   │   │   ├── ./share/bro/base/bif
│   │   │   │   ├── ./share/bro/base/bif/analyzer.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/bloom-filter.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/bro.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/broxygen.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/cardinality-counter.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/comm.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/const.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/data.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/event.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/file_analysis.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/input.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/__load__.bro
│   │   │   │   ├── ./share/bro/base/bif/logging.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/messaging.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/pcap.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/plugins
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_ARP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_AsciiReader.ascii.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_AsciiWriter.ascii.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_BackDoor.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_BenchmarkReader.benchmark.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_BinaryReader.binary.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_BitTorrent.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_ConnSize.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_ConnSize.functions.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_DCE_RPC.consts.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_DCE_RPC.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_DCE_RPC.types.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_DHCP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_DNP3.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_DNS.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_FileEntropy.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_File.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_FileExtract.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_FileExtract.functions.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_FileHash.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_Finger.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_FTP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_FTP.functions.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_Gnutella.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_GSSAPI.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_GTPv1.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_HTTP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_HTTP.functions.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_ICMP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_Ident.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_IMAP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_InterConn.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_IRC.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_KRB.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_KRB.types.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_Login.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_Login.functions.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_MIME.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_Modbus.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_MySQL.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_NCP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_NetBIOS.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_NetBIOS.functions.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_NoneWriter.none.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_NTLM.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_NTLM.types.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_NTP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_PE.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_POP3.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_RADIUS.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_RawReader.raw.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_RDP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_RDP.types.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_RFB.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_RPC.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SIP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.consts.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_check_directory.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_close.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_create_directory.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_echo.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_logoff_andx.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_negotiate.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_nt_cancel.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_nt_create_andx.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_query_information.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_read_andx.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_session_setup_andx.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_transaction2.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_transaction.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_tree_connect_andx.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_tree_disconnect.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_com_write_andx.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb1_events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb2_com_close.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb2_com_create.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb2_com_negotiate.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb2_com_read.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb2_com_session_setup.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb2_com_set_info.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb2_com_tree_connect.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb2_com_tree_disconnect.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb2_com_write.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.smb2_events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMB.types.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMTP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SMTP.functions.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SNMP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SNMP.types.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SOCKS.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SQLiteReader.sqlite.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SQLiteWriter.sqlite.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SSH.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SSH.types.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SSL.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SSL.functions.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SSL.types.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_SteppingStone.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_Syslog.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_TCP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_TCP.functions.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_Teredo.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_UDP.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_Unified2.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_Unified2.types.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_X509.events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_X509.functions.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_X509.ocsp_events.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_X509.types.bif.bro
│   │   │   │   │   ├── ./share/bro/base/bif/plugins/Bro_XMPP.events.bif.bro
│   │   │   │   │   └── ./share/bro/base/bif/plugins/__load__.bro
│   │   │   │   ├── ./share/bro/base/bif/reporter.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/stats.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/store.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/strings.bif.bro
│   │   │   │   ├── ./share/bro/base/bif/top-k.bif.bro
│   │   │   │   └── ./share/bro/base/bif/types.bif.bro
│   │   │   ├── ./share/bro/base/files
│   │   │   │   ├── ./share/bro/base/files/extract
│   │   │   │   │   ├── ./share/bro/base/files/extract/__load__.bro
│   │   │   │   │   └── ./share/bro/base/files/extract/main.bro
│   │   │   │   ├── ./share/bro/base/files/hash
│   │   │   │   │   ├── ./share/bro/base/files/hash/__load__.bro
│   │   │   │   │   └── ./share/bro/base/files/hash/main.bro
│   │   │   │   ├── ./share/bro/base/files/pe
│   │   │   │   │   ├── ./share/bro/base/files/pe/consts.bro
│   │   │   │   │   ├── ./share/bro/base/files/pe/__load__.bro
│   │   │   │   │   └── ./share/bro/base/files/pe/main.bro
│   │   │   │   ├── ./share/bro/base/files/unified2
│   │   │   │   │   ├── ./share/bro/base/files/unified2/__load__.bro
│   │   │   │   │   └── ./share/bro/base/files/unified2/main.bro
│   │   │   │   └── ./share/bro/base/files/x509
│   │   │   │       ├── ./share/bro/base/files/x509/__load__.bro
│   │   │   │       └── ./share/bro/base/files/x509/main.bro
│   │   │   ├── ./share/bro/base/frameworks
│   │   │   │   ├── ./share/bro/base/frameworks/analyzer
│   │   │   │   │   ├── ./share/bro/base/frameworks/analyzer/__load__.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/analyzer/main.bro
│   │   │   │   ├── ./share/bro/base/frameworks/broker
│   │   │   │   │   ├── ./share/bro/base/frameworks/broker/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/broker/main.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/broker/store.bro
│   │   │   │   ├── ./share/bro/base/frameworks/cluster
│   │   │   │   │   ├── ./share/bro/base/frameworks/cluster/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/cluster/main.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/cluster/nodes
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/cluster/nodes/logger.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/cluster/nodes/manager.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/cluster/nodes/proxy.bro
│   │   │   │   │   │   └── ./share/bro/base/frameworks/cluster/nodes/worker.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/cluster/setup-connections.bro
│   │   │   │   ├── ./share/bro/base/frameworks/communication
│   │   │   │   │   ├── ./share/bro/base/frameworks/communication/__load__.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/communication/main.bro
│   │   │   │   ├── ./share/bro/base/frameworks/control
│   │   │   │   │   ├── ./share/bro/base/frameworks/control/__load__.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/control/main.bro
│   │   │   │   ├── ./share/bro/base/frameworks/dpd
│   │   │   │   │   ├── ./share/bro/base/frameworks/dpd/__load__.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/dpd/main.bro
│   │   │   │   ├── ./share/bro/base/frameworks/files
│   │   │   │   │   ├── ./share/bro/base/frameworks/files/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/files/magic
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/files/magic/archive.sig
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/files/magic/audio.sig
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/files/magic/font.sig
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/files/magic/general.sig
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/files/magic/image.sig
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/files/magic/libmagic.sig
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/files/magic/__load__.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/files/magic/msoffice.sig
│   │   │   │   │   │   └── ./share/bro/base/frameworks/files/magic/video.sig
│   │   │   │   │   └── ./share/bro/base/frameworks/files/main.bro
│   │   │   │   ├── ./share/bro/base/frameworks/input
│   │   │   │   │   ├── ./share/bro/base/frameworks/input/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/input/main.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/input/readers
│   │   │   │   │       ├── ./share/bro/base/frameworks/input/readers/ascii.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/input/readers/benchmark.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/input/readers/binary.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/input/readers/raw.bro
│   │   │   │   │       └── ./share/bro/base/frameworks/input/readers/sqlite.bro
│   │   │   │   ├── ./share/bro/base/frameworks/intel
│   │   │   │   │   ├── ./share/bro/base/frameworks/intel/cluster.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/intel/files.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/intel/input.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/intel/__load__.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/intel/main.bro
│   │   │   │   ├── ./share/bro/base/frameworks/logging
│   │   │   │   │   ├── ./share/bro/base/frameworks/logging/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/logging/main.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/logging/postprocessors
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/logging/postprocessors/__load__.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/logging/postprocessors/scp.bro
│   │   │   │   │   │   └── ./share/bro/base/frameworks/logging/postprocessors/sftp.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/logging/writers
│   │   │   │   │       ├── ./share/bro/base/frameworks/logging/writers/ascii.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/logging/writers/none.bro
│   │   │   │   │       └── ./share/bro/base/frameworks/logging/writers/sqlite.bro
│   │   │   │   ├── ./share/bro/base/frameworks/netcontrol
│   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/catch-and-release.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/cluster.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/drop.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/main.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/non-cluster.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/plugin.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/plugins
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/plugins/acld.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/plugins/broker.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/plugins/debug.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/plugins/__load__.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/plugins/openflow.bro
│   │   │   │   │   │   └── ./share/bro/base/frameworks/netcontrol/plugins/packetfilter.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/netcontrol/shunt.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/netcontrol/types.bro
│   │   │   │   ├── ./share/bro/base/frameworks/notice
│   │   │   │   │   ├── ./share/bro/base/frameworks/notice/actions
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/notice/actions/add-geodata.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/notice/actions/drop.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/notice/actions/email_admin.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/notice/actions/page.bro
│   │   │   │   │   │   └── ./share/bro/base/frameworks/notice/actions/pp-alarms.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/notice/cluster.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/notice/extend-email
│   │   │   │   │   │   └── ./share/bro/base/frameworks/notice/extend-email/hostnames.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/notice/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/notice/main.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/notice/non-cluster.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/notice/weird.bro
│   │   │   │   ├── ./share/bro/base/frameworks/openflow
│   │   │   │   │   ├── ./share/bro/base/frameworks/openflow/cluster.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/openflow/consts.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/openflow/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/openflow/main.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/openflow/non-cluster.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/openflow/plugins
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/openflow/plugins/broker.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/openflow/plugins/__load__.bro
│   │   │   │   │   │   ├── ./share/bro/base/frameworks/openflow/plugins/log.bro
│   │   │   │   │   │   └── ./share/bro/base/frameworks/openflow/plugins/ryu.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/openflow/types.bro
│   │   │   │   ├── ./share/bro/base/frameworks/packet-filter
│   │   │   │   │   ├── ./share/bro/base/frameworks/packet-filter/cluster.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/packet-filter/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/packet-filter/main.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/packet-filter/netstats.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/packet-filter/utils.bro
│   │   │   │   ├── ./share/bro/base/frameworks/reporter
│   │   │   │   │   ├── ./share/bro/base/frameworks/reporter/__load__.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/reporter/main.bro
│   │   │   │   ├── ./share/bro/base/frameworks/signatures
│   │   │   │   │   ├── ./share/bro/base/frameworks/signatures/__load__.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/signatures/main.bro
│   │   │   │   ├── ./share/bro/base/frameworks/software
│   │   │   │   │   ├── ./share/bro/base/frameworks/software/__load__.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/software/main.bro
│   │   │   │   ├── ./share/bro/base/frameworks/sumstats
│   │   │   │   │   ├── ./share/bro/base/frameworks/sumstats/cluster.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/sumstats/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/sumstats/main.bro
│   │   │   │   │   ├── ./share/bro/base/frameworks/sumstats/non-cluster.bro
│   │   │   │   │   └── ./share/bro/base/frameworks/sumstats/plugins
│   │   │   │   │       ├── ./share/bro/base/frameworks/sumstats/plugins/average.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/sumstats/plugins/hll_unique.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/sumstats/plugins/last.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/sumstats/plugins/__load__.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/sumstats/plugins/max.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/sumstats/plugins/min.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/sumstats/plugins/sample.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/sumstats/plugins/std-dev.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/sumstats/plugins/sum.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/sumstats/plugins/topk.bro
│   │   │   │   │       ├── ./share/bro/base/frameworks/sumstats/plugins/unique.bro
│   │   │   │   │       └── ./share/bro/base/frameworks/sumstats/plugins/variance.bro
│   │   │   │   └── ./share/bro/base/frameworks/tunnels
│   │   │   │       ├── ./share/bro/base/frameworks/tunnels/__load__.bro
│   │   │   │       └── ./share/bro/base/frameworks/tunnels/main.bro
│   │   │   ├── ./share/bro/base/init-bare.bro
│   │   │   ├── ./share/bro/base/init-default.bro
│   │   │   ├── ./share/bro/base/misc
│   │   │   │   ├── ./share/bro/base/misc/find-checksum-offloading.bro
│   │   │   │   ├── ./share/bro/base/misc/find-filtered-trace.bro
│   │   │   │   ├── ./share/bro/base/misc/p0f.fp
│   │   │   │   └── ./share/bro/base/misc/version.bro
│   │   │   ├── ./share/bro/base/protocols
│   │   │   │   ├── ./share/bro/base/protocols/conn
│   │   │   │   │   ├── ./share/bro/base/protocols/conn/contents.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/conn/inactivity.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/conn/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/conn/main.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/conn/polling.bro
│   │   │   │   │   └── ./share/bro/base/protocols/conn/thresholds.bro
│   │   │   │   ├── ./share/bro/base/protocols/dce-rpc
│   │   │   │   │   ├── ./share/bro/base/protocols/dce-rpc/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/dce-rpc/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/dce-rpc/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/dce-rpc/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/dhcp
│   │   │   │   │   ├── ./share/bro/base/protocols/dhcp/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/dhcp/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/dhcp/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/dhcp/main.bro
│   │   │   │   │   └── ./share/bro/base/protocols/dhcp/utils.bro
│   │   │   │   ├── ./share/bro/base/protocols/dnp3
│   │   │   │   │   ├── ./share/bro/base/protocols/dnp3/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/dnp3/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/dnp3/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/dnp3/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/dns
│   │   │   │   │   ├── ./share/bro/base/protocols/dns/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/dns/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/dns/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/ftp
│   │   │   │   │   ├── ./share/bro/base/protocols/ftp/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/ftp/files.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/ftp/gridftp.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/ftp/info.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/ftp/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/ftp/main.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/ftp/utils.bro
│   │   │   │   │   └── ./share/bro/base/protocols/ftp/utils-commands.bro
│   │   │   │   ├── ./share/bro/base/protocols/http
│   │   │   │   │   ├── ./share/bro/base/protocols/http/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/http/entities.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/http/files.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/http/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/http/main.bro
│   │   │   │   │   └── ./share/bro/base/protocols/http/utils.bro
│   │   │   │   ├── ./share/bro/base/protocols/imap
│   │   │   │   │   ├── ./share/bro/base/protocols/imap/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/imap/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/irc
│   │   │   │   │   ├── ./share/bro/base/protocols/irc/dcc-send.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/irc/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/irc/files.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/irc/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/irc/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/krb
│   │   │   │   │   ├── ./share/bro/base/protocols/krb/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/krb/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/krb/files.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/krb/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/krb/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/modbus
│   │   │   │   │   ├── ./share/bro/base/protocols/modbus/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/modbus/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/modbus/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/mysql
│   │   │   │   │   ├── ./share/bro/base/protocols/mysql/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/mysql/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/mysql/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/ntlm
│   │   │   │   │   ├── ./share/bro/base/protocols/ntlm/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/ntlm/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/pop3
│   │   │   │   │   ├── ./share/bro/base/protocols/pop3/dpd.sig
│   │   │   │   │   └── ./share/bro/base/protocols/pop3/__load__.bro
│   │   │   │   ├── ./share/bro/base/protocols/radius
│   │   │   │   │   ├── ./share/bro/base/protocols/radius/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/radius/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/radius/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/rdp
│   │   │   │   │   ├── ./share/bro/base/protocols/rdp/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/rdp/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/rdp/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/rdp/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/rfb
│   │   │   │   │   ├── ./share/bro/base/protocols/rfb/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/rfb/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/rfb/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/sip
│   │   │   │   │   ├── ./share/bro/base/protocols/sip/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/sip/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/sip/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/smb
│   │   │   │   │   ├── ./share/bro/base/protocols/smb/const-dos-error.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/smb/const-nt-status.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/smb/consts.bro
│   │   │   │   │   └── ./share/bro/base/protocols/smb/__load__.bro
│   │   │   │   ├── ./share/bro/base/protocols/smtp
│   │   │   │   │   ├── ./share/bro/base/protocols/smtp/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/smtp/entities.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/smtp/files.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/smtp/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/smtp/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/snmp
│   │   │   │   │   ├── ./share/bro/base/protocols/snmp/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/snmp/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/socks
│   │   │   │   │   ├── ./share/bro/base/protocols/socks/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/socks/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/socks/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/socks/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/ssh
│   │   │   │   │   ├── ./share/bro/base/protocols/ssh/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/ssh/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/ssh/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/ssl
│   │   │   │   │   ├── ./share/bro/base/protocols/ssl/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/ssl/ct-list.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/ssl/dpd.sig
│   │   │   │   │   ├── ./share/bro/base/protocols/ssl/files.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/ssl/__load__.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/ssl/main.bro
│   │   │   │   │   └── ./share/bro/base/protocols/ssl/mozilla-ca-list.bro
│   │   │   │   ├── ./share/bro/base/protocols/syslog
│   │   │   │   │   ├── ./share/bro/base/protocols/syslog/consts.bro
│   │   │   │   │   ├── ./share/bro/base/protocols/syslog/__load__.bro
│   │   │   │   │   └── ./share/bro/base/protocols/syslog/main.bro
│   │   │   │   ├── ./share/bro/base/protocols/tunnels
│   │   │   │   │   ├── ./share/bro/base/protocols/tunnels/dpd.sig
│   │   │   │   │   └── ./share/bro/base/protocols/tunnels/__load__.bro
│   │   │   │   └── ./share/bro/base/protocols/xmpp
│   │   │   │       ├── ./share/bro/base/protocols/xmpp/dpd.sig
│   │   │   │       ├── ./share/bro/base/protocols/xmpp/__load__.bro
│   │   │   │       └── ./share/bro/base/protocols/xmpp/main.bro
│   │   │   └── ./share/bro/base/utils
│   │   │       ├── ./share/bro/base/utils/active-http.bro
│   │   │       ├── ./share/bro/base/utils/addrs.bro
│   │   │       ├── ./share/bro/base/utils/conn-ids.bro
│   │   │       ├── ./share/bro/base/utils/dir.bro
│   │   │       ├── ./share/bro/base/utils/directions-and-hosts.bro
│   │   │       ├── ./share/bro/base/utils/email.bro
│   │   │       ├── ./share/bro/base/utils/exec.bro
│   │   │       ├── ./share/bro/base/utils/files.bro
│   │   │       ├── ./share/bro/base/utils/geoip-distance.bro
│   │   │       ├── ./share/bro/base/utils/json.bro
│   │   │       ├── ./share/bro/base/utils/numbers.bro
│   │   │       ├── ./share/bro/base/utils/paths.bro
│   │   │       ├── ./share/bro/base/utils/patterns.bro
│   │   │       ├── ./share/bro/base/utils/queue.bro
│   │   │       ├── ./share/bro/base/utils/site.bro
│   │   │       ├── ./share/bro/base/utils/strings.bro
│   │   │       ├── ./share/bro/base/utils/thresholds.bro
│   │   │       ├── ./share/bro/base/utils/time.bro
│   │   │       └── ./share/bro/base/utils/urls.bro
│   │   ├── ./share/bro/broctl
│   │   │   ├── ./share/bro/broctl/auto.bro
│   │   │   ├── ./share/bro/broctl/check.bro
│   │   │   ├── ./share/bro/broctl/__load__.bro
│   │   │   ├── ./share/bro/broctl/main.bro
│   │   │   ├── ./share/bro/broctl/process-trace.bro
│   │   │   └── ./share/bro/broctl/standalone.bro
│   │   ├── ./share/bro/broxygen
│   │   │   ├── ./share/bro/broxygen/example.bro
│   │   │   └── ./share/bro/broxygen/__load__.bro
│   │   ├── ./share/bro/policy  # 需要指定才加载的脚本
│   │   │   ├── ./share/bro/policy/files
│   │   │   │   └── ./share/bro/policy/files/x509
│   │   │   │       └── ./share/bro/policy/files/x509/log-ocsp.bro
│   │   │   ├── ./share/bro/policy/frameworks
│   │   │   │   ├── ./share/bro/policy/frameworks/communication
│   │   │   │   │   └── ./share/bro/policy/frameworks/communication/listen.bro
│   │   │   │   ├── ./share/bro/policy/frameworks/control
│   │   │   │   │   ├── ./share/bro/policy/frameworks/control/controllee.bro
│   │   │   │   │   └── ./share/bro/policy/frameworks/control/controller.bro
│   │   │   │   ├── ./share/bro/policy/frameworks/dpd
│   │   │   │   │   ├── ./share/bro/policy/frameworks/dpd/detect-protocols.bro
│   │   │   │   │   └── ./share/bro/policy/frameworks/dpd/packet-segment-logging.bro
│   │   │   │   ├── ./share/bro/policy/frameworks/files
│   │   │   │   │   ├── ./share/bro/policy/frameworks/files/detect-MHR.bro
│   │   │   │   │   ├── ./share/bro/policy/frameworks/files/entropy-test-all-files.bro
│   │   │   │   │   ├── ./share/bro/policy/frameworks/files/extract-all-files.bro
│   │   │   │   │   └── ./share/bro/policy/frameworks/files/hash-all-files.bro
│   │   │   │   ├── ./share/bro/policy/frameworks/intel
│   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/do_expire.bro
│   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/do_notice.bro
│   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/conn-established.bro
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/dns.bro
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/file-hashes.bro
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/file-names.bro
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/http-headers.bro
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/http-url.bro
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/__load__.bro
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/pubkey-hashes.bro
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/smtp.bro
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/smtp-url-extraction.bro
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/ssl.bro
│   │   │   │   │   │   ├── ./share/bro/policy/frameworks/intel/seen/where-locations.bro
│   │   │   │   │   │   └── ./share/bro/policy/frameworks/intel/seen/x509.bro
│   │   │   │   │   └── ./share/bro/policy/frameworks/intel/whitelist.bro
│   │   │   │   ├── ./share/bro/policy/frameworks/packet-filter
│   │   │   │   │   └── ./share/bro/policy/frameworks/packet-filter/shunt.bro
│   │   │   │   ├── ./share/bro/policy/frameworks/signatures
│   │   │   │   │   └── ./share/bro/policy/frameworks/signatures/detect-windows-shells.sig
│   │   │   │   └── ./share/bro/policy/frameworks/software
│   │   │   │       ├── ./share/bro/policy/frameworks/software/version-changes.bro
│   │   │   │       ├── ./share/bro/policy/frameworks/software/vulnerable.bro
│   │   │   │       └── ./share/bro/policy/frameworks/software/windows-version-detection.bro
│   │   │   ├── ./share/bro/policy/integration
│   │   │   │   ├── ./share/bro/policy/integration/barnyard2
│   │   │   │   │   ├── ./share/bro/policy/integration/barnyard2/__load__.bro
│   │   │   │   │   ├── ./share/bro/policy/integration/barnyard2/main.bro
│   │   │   │   │   └── ./share/bro/policy/integration/barnyard2/types.bro
│   │   │   │   └── ./share/bro/policy/integration/collective-intel
│   │   │   │       ├── ./share/bro/policy/integration/collective-intel/__load__.bro
│   │   │   │       └── ./share/bro/policy/integration/collective-intel/main.bro
│   │   │   ├── ./share/bro/policy/misc
│   │   │   │   ├── ./share/bro/policy/misc/capture-loss.bro
│   │   │   │   ├── ./share/bro/policy/misc/detect-traceroute
│   │   │   │   │   ├── ./share/bro/policy/misc/detect-traceroute/detect-low-ttls.sig
│   │   │   │   │   ├── ./share/bro/policy/misc/detect-traceroute/__load__.bro
│   │   │   │   │   └── ./share/bro/policy/misc/detect-traceroute/main.bro
│   │   │   │   ├── ./share/bro/policy/misc/dump-events.bro
│   │   │   │   ├── ./share/bro/policy/misc/known-devices.bro
│   │   │   │   ├── ./share/bro/policy/misc/load-balancing.bro
│   │   │   │   ├── ./share/bro/policy/misc/loaded-scripts.bro
│   │   │   │   ├── ./share/bro/policy/misc/profiling.bro
│   │   │   │   ├── ./share/bro/policy/misc/scan.bro
│   │   │   │   ├── ./share/bro/policy/misc/stats.bro
│   │   │   │   └── ./share/bro/policy/misc/trim-trace-file.bro
│   │   │   ├── ./share/bro/policy/protocols
│   │   │   │   ├── ./share/bro/policy/protocols/conn
│   │   │   │   │   ├── ./share/bro/policy/protocols/conn/known-hosts.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/conn/known-services.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/conn/mac-logging.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/conn/vlan-logging.bro
│   │   │   │   │   └── ./share/bro/policy/protocols/conn/weirds.bro
│   │   │   │   ├── ./share/bro/policy/protocols/dhcp
│   │   │   │   │   └── ./share/bro/policy/protocols/dhcp/known-devices-and-hostnames.bro
│   │   │   │   ├── ./share/bro/policy/protocols/dns
│   │   │   │   │   ├── ./share/bro/policy/protocols/dns/auth-addl.bro
│   │   │   │   │   └── ./share/bro/policy/protocols/dns/detect-external-names.bro
│   │   │   │   ├── ./share/bro/policy/protocols/ftp
│   │   │   │   │   ├── ./share/bro/policy/protocols/ftp/detect.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/ftp/detect-bruteforcing.bro
│   │   │   │   │   └── ./share/bro/policy/protocols/ftp/software.bro
│   │   │   │   ├── ./share/bro/policy/protocols/http
│   │   │   │   │   ├── ./share/bro/policy/protocols/http/detect-sqli.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/http/detect-webapps.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/http/detect-webapps.sig
│   │   │   │   │   ├── ./share/bro/policy/protocols/http/header-names.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/http/software.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/http/software-browser-plugins.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/http/var-extraction-cookies.bro
│   │   │   │   │   └── ./share/bro/policy/protocols/http/var-extraction-uri.bro
│   │   │   │   ├── ./share/bro/policy/protocols/krb
│   │   │   │   │   └── ./share/bro/policy/protocols/krb/ticket-logging.bro
│   │   │   │   ├── ./share/bro/policy/protocols/modbus
│   │   │   │   │   ├── ./share/bro/policy/protocols/modbus/known-masters-slaves.bro
│   │   │   │   │   └── ./share/bro/policy/protocols/modbus/track-memmap.bro
│   │   │   │   ├── ./share/bro/policy/protocols/mysql
│   │   │   │   │   └── ./share/bro/policy/protocols/mysql/software.bro
│   │   │   │   ├── ./share/bro/policy/protocols/rdp
│   │   │   │   │   └── ./share/bro/policy/protocols/rdp/indicate_ssl.bro
│   │   │   │   ├── ./share/bro/policy/protocols/smb
│   │   │   │   │   ├── ./share/bro/policy/protocols/smb/dpd.sig
│   │   │   │   │   ├── ./share/bro/policy/protocols/smb/files.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/smb/__load__.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/smb/main.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/smb/smb1-main.bro
│   │   │   │   │   └── ./share/bro/policy/protocols/smb/smb2-main.bro
│   │   │   │   ├── ./share/bro/policy/protocols/smtp
│   │   │   │   │   ├── ./share/bro/policy/protocols/smtp/blocklists.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/smtp/detect-suspicious-orig.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/smtp/entities-excerpt.bro
│   │   │   │   │   └── ./share/bro/policy/protocols/smtp/software.bro
│   │   │   │   ├── ./share/bro/policy/protocols/ssh
│   │   │   │   │   ├── ./share/bro/policy/protocols/ssh/detect-bruteforcing.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/ssh/geo-data.bro
│   │   │   │   │   ├── ./share/bro/policy/protocols/ssh/interesting-hostnames.bro
│   │   │   │   │   └── ./share/bro/policy/protocols/ssh/software.bro
│   │   │   │   └── ./share/bro/policy/protocols/ssl
│   │   │   │       ├── ./share/bro/policy/protocols/ssl/expiring-certs.bro
│   │   │   │       ├── ./share/bro/policy/protocols/ssl/extract-certs-pem.bro
│   │   │   │       ├── ./share/bro/policy/protocols/ssl/heartbleed.bro
│   │   │   │       ├── ./share/bro/policy/protocols/ssl/known-certs.bro
│   │   │   │       ├── ./share/bro/policy/protocols/ssl/log-hostcerts-only.bro
│   │   │   │       ├── ./share/bro/policy/protocols/ssl/notary.bro
│   │   │   │       ├── ./share/bro/policy/protocols/ssl/validate-certs.bro
│   │   │   │       ├── ./share/bro/policy/protocols/ssl/validate-ocsp.bro
│   │   │   │       ├── ./share/bro/policy/protocols/ssl/validate-sct.bro
│   │   │   │       └── ./share/bro/policy/protocols/ssl/weak-keys.bro
│   │   │   └── ./share/bro/policy/tuning
│   │   │       ├── ./share/bro/policy/tuning/defaults
│   │   │       │   ├── ./share/bro/policy/tuning/defaults/extracted_file_limits.bro
│   │   │       │   ├── ./share/bro/policy/tuning/defaults/__load__.bro
│   │   │       │   ├── ./share/bro/policy/tuning/defaults/packet-fragments.bro
│   │   │       │   └── ./share/bro/policy/tuning/defaults/warnings.bro
│   │   │       ├── ./share/bro/policy/tuning/json-logs.bro
│   │   │       ├── ./share/bro/policy/tuning/__load__.bro
│   │   │       └── ./share/bro/policy/tuning/track-all-assets.bro
│   │   └── ./share/bro/site
│   │       ├── ./share/bro/site/local.bro
│   │       ├── ./share/bro/site/local-logger.bro
│   │       ├── ./share/bro/site/local-manager.bro
│   │       ├── ./share/bro/site/local-proxy.bro
│   │       └── ./share/bro/site/local-worker.bro
│   ├── ./share/broctl
│   │   └── ./share/broctl/scripts
│   │       ├── ./share/broctl/scripts/archive-log
│   │       ├── ./share/broctl/scripts/broctl-config.sh -> /usr/local/bro/spool/broctl-config.sh
│   │       ├── ./share/broctl/scripts/check-config
│   │       ├── ./share/broctl/scripts/crash-diag
│   │       ├── ./share/broctl/scripts/delete-log
│   │       ├── ./share/broctl/scripts/expire-crash
│   │       ├── ./share/broctl/scripts/expire-logs
│   │       ├── ./share/broctl/scripts/helpers
│   │       │   ├── ./share/broctl/scripts/helpers/check-pid
│   │       │   ├── ./share/broctl/scripts/helpers/df
│   │       │   ├── ./share/broctl/scripts/helpers/first-line
│   │       │   ├── ./share/broctl/scripts/helpers/get-childs
│   │       │   ├── ./share/broctl/scripts/helpers/start
│   │       │   ├── ./share/broctl/scripts/helpers/stop
│   │       │   ├── ./share/broctl/scripts/helpers/to-bytes.awk
│   │       │   └── ./share/broctl/scripts/helpers/top
│   │       ├── ./share/broctl/scripts/make-archive-name
│   │       ├── ./share/broctl/scripts/postprocessors
│   │       │   └── ./share/broctl/scripts/postprocessors/summarize-connections
│   │       ├── ./share/broctl/scripts/post-terminate
│   │       ├── ./share/broctl/scripts/run-bro
│   │       ├── ./share/broctl/scripts/run-bro-on-trace
│   │       ├── ./share/broctl/scripts/send-mail
│   │       ├── ./share/broctl/scripts/set-bro-path
│   │       ├── ./share/broctl/scripts/stats-to-csv
│   │       └── ./share/broctl/scripts/update
│   └── ./share/man
│       ├── ./share/man/man1
│       │   ├── ./share/man/man1/bro-cut.1
│       │   └── ./share/man/man1/trace-summary.1
│       └── ./share/man/man8
│           ├── ./share/man/man8/bro.8
│           └── ./share/man/man8/broctl.8
└── ./spool
    ├── ./spool/bro
    ├── ./spool/broctl-config.sh
    ├── ./spool/debug.log
    ├── ./spool/installed-scripts-do-not-touch
    │   ├── ./spool/installed-scripts-do-not-touch/auto
    │   │   ├── ./spool/installed-scripts-do-not-touch/auto/broctl-config.bro
    │   │   ├── ./spool/installed-scripts-do-not-touch/auto/local-networks.bro
    │   │   └── ./spool/installed-scripts-do-not-touch/auto/standalone-layout.bro
    │   └── ./spool/installed-scripts-do-not-touch/site
    │       ├── ./spool/installed-scripts-do-not-touch/site/local.bro
    │       ├── ./spool/installed-scripts-do-not-touch/site/local-logger.bro
    │       ├── ./spool/installed-scripts-do-not-touch/site/local-manager.bro
    │       ├── ./spool/installed-scripts-do-not-touch/site/local-proxy.bro
    │       └── ./spool/installed-scripts-do-not-touch/site/local-worker.bro
    ├── ./spool/state.db
    └── ./spool/tmp
        └── ./spool/tmp/post-terminate-standalone-2018-01-08-20-28-51-16739-crash
            └── ./spool/tmp/post-terminate-standalone-2018-01-08-20-28-51-16739-crash/post-terminate.out

134 directories, 625 files

```

