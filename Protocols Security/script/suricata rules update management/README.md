


# 规则更新流程

## 1 检查官方规则更新

sr_compare.py下载官方rules文件并与本地rules文件比较，生成log文件

```bash
python3 sr_compare.py all # 下载并比较em官方规则
python3 sr_compare.py pt # 下载并比较pt规则
```
也可用`python3 sr_compare.py emerging-web_specific_apps.rules struts`，只查看指定keyword的规则更新。

## 2 人工审查规则

人工审查规则，其中不更新的规则，则删除前面的"official"或"add"字眼，在"==="后可以加上规则备注。



sr_test.py 将log生成为rules文件，用于测试。

```bash
python3 SR_Test.py struts # 提取keyword相关规则生成rules
python3 SR_Test.py sid 12345 24567 # 提取指定规则生成rules
python3 SR_Test.py log pt-rules.rules.log # 提取log文件中的规则生成rules
```

## 3 更新规则

sr_replace.py 将log文件中的update和add添加到本地rules中。，把add但是删除的情况以注释的形式加进去。

```python
def name():
    # 不需要被更新的规则的 sid
    no update_list = []
    # 新增规则的 sid
    new_add_list = []

    pass

    return no_update_list, new_add_list
```


## ToDo

sid