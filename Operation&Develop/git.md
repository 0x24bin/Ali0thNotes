# GIT

## git安装

yum install git

## git更新

配置你的账户：
```s
git config --global user.name 'runoob'
git config --global user.email test@runoob.com
```

> git status（查看本地分支文件信息，确保更新时不产生冲突）

> git clone

指定远程主机的名字 : git clone -o name http://192.168.72.128/root/test.git

> git remote

查看远程主机 : git remote -v 

删除 : git remote rm <主机名>

> git fetch 取回更新，不合并

查看远程分支 : git branch -r

查看所有分支 : git branch -a

取回origin主机的master分支 : git fetch origin master


合并master : 

```
pick：正常选中
reword：选中，并且修改提交信息；
edit：选中，rebase时会暂停，允许你修改这个commit（参考这里）
squash：选中，会将当前commit与上一个commit合并
fixup：与squash相同，但不会保存当前commit的提交信息
exec：执行其他shell命令
```

合并远程分支 : $ git merge origin/master

$ git rebase origin/master

排除不合并的 : git rebase -i 123

> git branch
```s

创建分支 $ git branch <branch-name>

查看分支 $ git branch

切换分支 $ git checkout <branch-name>

创建并切换到新分支 $ git checkout -b <branch-name>

git checkout -b newBrach origin/master

删除分支 $ git branch -d <branch-name>
```

> git commit

git add <file>

命令用于取消已缓存的内容 : git reset HEAD

git commit <file>

git commit -a

提交至本地仓库 : git commit -m '备注信息'




> git pull 取回更新，合并

取回远程主机某个分支的更新，再与本地的指定分支合并 : $ git pull <远程主机名> <远程分支名>:<本地分支名>

取回origin主机的next分支，与本地的master分支合并 : $ git pull origin next:master

远程分支是与当前分支合并 : $ git pull origin next

> git push <远程主机名> <本地分支名>:<远程分支名>

推送本地到master : git push origin master

推送本地到master : git push origin newBranch

将当前分支推送到origin主机的对应分支 : git push origin


# 资料

Git远程操作详解

http://www.ruanyifeng.com/blog/2014/06/git_remote.html

git常见操作

http://www.cnblogs.com/elfsundae/archive/2011/07/17/2099698.html