# GitLab

Gitlab是一个利用Ruby on Rails开发的开源应用程序，实现了一个自托管的Git项目仓库，可通过Web界面进行访问公开的或者私人项目。

安装：https://about.gitlab.com/installation

## 操作Tips:

查看gitlab版本：登录后，访问`domain.com/help`

## 测试环境：

Gitlab CE 8.10.3

https://www.ichunqiu.com/vm/57891/1

Gitlab CE 8.13.1

https://github.com/vulhub/vulhub/tree/master/gitlab/CVE-2016-9086

GitLab CE 9.3.5

git.tophant.com

GitLab CE 10.1.2

https://58.240.177.119/gitlab/help

9.5.4

http://gitlab.laserbeam897.tk/help

xxx

http://101.200.219.201:8000/anjing/gitlab-tutorial

## 资料

update blog

https://about.gitlab.com/blog/archives.html

hackone gitlab

https://hackerone.com/gitlab/hacktivity?sort_type=latest_disclosable_activity_at&filter=type%3Aall%20to%3Agitlab&page=1&range=forever

更新日志(搜`Security`即可知漏洞)

https://gitlab.com/gitlab-org/gitlab-ce/raw/master/CHANGELOG.md

## 任意文件读取漏洞(CVE-2016-9086)

GitLab CE/EE versions 8.9, 8.10, 8.11, 8.12, and 8.13

### 漏洞利用过程

1. project export并解压
2. 删除掉`2017-03-30_22-18-835_test_test_export.tar.gz`及`project.json`(删除的命令为rm 文件名)，然后将`/etc/passwd`软连接到当前目录的`project.json`.输入`ln -sf /etc/passwd project.json`
3. 将软连接做好之后，重新打包回tar.gz，`tar zcf poc.tar.gz ./`
4. 导入project

### 漏洞原理

当我们导入GitLab的导出文件的时候，GitLab会按照如下步骤处理： 
1. 服务器根据`VERSION`文件内容检测导出文件版本，如果版本符合，则导入。
2. 服务器根据`Project.json`文件创建一个新的项目，并将对应的项目文件拷贝到服务器上对应的位置。

检测VERSION文件的代码位于：`/lib/gitlab/import_export/version_checker.rb`中：
```ruby
      def check!
        version = File.open(version_file, &:readline)
        verify_version!(version)
      rescue => e
        @shared.error(e)
        false
      end
```
这里的逻辑是读取VERSION文件的第一行赋值给变量version，然后检测verison与当前版本是否相同，相同返回true，不相同则返回错误信息(错误信息中包括变量version的值). 所以VERSION是可以利的，使用`ln -sf /etc/passwd VERSION`，不过只能读到一行信息。

而project.json可以读取多行信息。读取 project.json 这一配置文件的代码位于：`/lib/gitlab/import_export/project_tree_restorer.rb`中：

```ruby
def restore
  json = IO.read(@path)
  tree_hash = ActiveSupport::JSON.decode(json)
  project_members = tree_hash.delete('project_members')

  ActiveRecord::Base.no_touchingdo
    create_relations
  end
rescue => e  
  shared.error(e)
  false
end
```
在这里，我们可以使用软链接使变量json获取到任意文件的内容，但是由于获取的文件不是json格式，无法decode，导致异常抛出，最终在前端显示出任意文件的内容。


## 任意用户authentication_token泄露漏洞

Gitlab CE/EE versions 8.10.3-8.10.5

### 漏洞利用过程

1. 注册一个普通用户，创建一个新的项目
2. 在项目的member选项中，添加管理员到项目中。
3. project export并解压
4. project.json中已经含有了管理员的authentication_token
5. 得到authentication_token之后我们就可以通过api做管理员可以做的事情了,比如查看管理员所在的项目：`domain.com/api/v3/projects?private_token=XXX` 或 `domain.com/admin/users?authentication_token=XXX`

### 漏洞原理

### 资料

GitLab 任意文件读取漏洞 (CVE-2016-9086) 视频

https://www.ichunqiu.com/course/57887

GitLab 任意文件读取漏洞 (CVE-2016-9086) 和任意用户 token 泄露漏洞 分析

http://blog.knownsec.com/2016/11/gitlab-file-read-vulnerability-cve-2016-9086-and-access-all-user-authentication-token/


## Remote Command Execution in git client (CVE-2017-12426)

### 影响

7.9.0 through 8.17.7

9.0.0 through 9.0.12

9.1.0 through 9.1.9

9.2.0 through 9.2.9

9.3.0 through 9.3.9

9.4.0 through 9.4.3

### 利用过程

1. Click New Project, fill out a project name.
2. Click git Repo by URL.
3. Paste a URL like `ssh://-oProxyCommand=[snip]/a`.
4. Click Create project


### 缓解方案

移除ssh协议

For source users edit: `/app/validators/addressable_url_validator.rb`

For Omnibus users edit: `/opt/gitlab/embedded/service/gitlab-rails/app/validators/addressable_url_validator.rb`

Change:

`DEFAULT_OPTIONS = { protocols: %w(http https ssh git) }.freeze`

To:

`DEFAULT_OPTIONS = { protocols: %w(http https git) }.freeze`

Then restart GitLab.For Omnibus users: gitlab-ctl restart.

### 漏洞原理


### 资料

Remote Command Execution (RCE) in project import

https://gitlab.com/gitlab-org/gitlab-ce/issues/35212

Remote Command Execution in git client (CVE-2017-12426)

https://www.seebug.org/vuldb/ssvid-96341


## GitLab 权限泄露漏洞（CVE-2017-0882)

当修改任务的分配者信息的时候，API 将返回该用户的个人信息详情，其中包括了该用户的authentication_token、encrypted_otp_secret、otp_backup_codes等敏感信息。

使用这些敏感信息结合 Gitlab API 可以实现使用该用户的身份和权限操作 GitLab。如果用户为管理员权限，可能会造成更大的危害。

### 影响

8.7.0 through 8.15.7

8.16.0 through 8.16.7

8.17.0 through 8.17.3

### 利用过程

1. Browse to a project
2. Open the project's issue tracker
3. Create an issue and assign ownership of the issue to another user
4. View the returned JSON

(或是已有别人的issue可以直接点击issue查看返回的JSON)

### 资料

https://www.seebug.org/vuldb/ssvid-92805

https://gitlab.com/gitlab-org/gitlab-ce/issues/29661













## 多个漏洞研究

https://about.gitlab.com/2018/01/16/gitlab-10-dot-3-dot-4-released/

https://about.gitlab.com/2017/08/10/gitlab-9-dot-4-dot-4-released/


影响：

GitLab CE and EE 8.8.0 - 10.1.5

GitLab CE and EE 10.2.0 - 10.2.5

GitLab CE and EE 10.3.0 - 10.3.3

Fix:

https://gitlab.com/gitlab-org/gitlab-ce/commit/f58e165b2afb7718ecbdbf50201a394217e269b3

https://gitlab.com/gitlab-org/gitlab-ce/commit/7c4f7c283d8ae69ddfdc5feefbe31aab12906ffe

https://gitlab.com/gitlab-org/gitlab-ce/commit/056d35cad0e09a59fdf44cb6bd7063f73a970f01

下载：

https://github.com/gitlabhq/gitlabhq/releases/tag/v10.3.4

https://github.com/gitlabhq/gitlabhq/releases/tag/v10.3.3

9.3.9

https://hub.docker.com/r/gotfix/gitlab/


## GitLab 项目导入中的远程代码执行漏洞

GitLab 项目导入组件包含一个漏洞，该漏洞允许攻击者将文件写入服务器上的任意目录，并可能导致远程执行代码。对于此漏洞，该版本已提供有效的漏洞缓解措施，并将其标记为 CVE-2017-0915 和 CVE-2018-3710。

受影响的版本

GitLab CE and EE 8.9.0 - 9.5.10

GitLab CE and EE 10.0.0 - 10.1.5

GitLab CE and EE 10.2.0 - 10.2.5

GitLab CE and EE 10.3.0 - 10.3.3

临时解决方案

1. Go to `/admin/application_settings` of your GitLab instance.
2. Under "Import sources", uncheck the "GitLab export" checkbox.
3. Click Save.


## GitLab CI Runner 可读取所有其他项目的缓存（CVE-2017-0918）

在 CI runner 中发现了一个路径遍历漏洞，该漏洞允许恶意用户读取其他项目缓存。此漏洞现已被修复，并被标记为 CVE-2017-0918。

受影响的版本

GitLab CE and EE 8.4.0 - 9.5.10

GitLab CE and EE 10.0.0 - 10.1.5

GitLab CE and EE 10.2.0 - 10.2.5

GitLab CE and EE 10.3.0 - 10.3.3


## Jupyter Notebook XSS（CVE-2017-0923）

具有 Jupyter Notebooks 的项目可以执行外部 JavaScript。这个 XSS 漏洞是由 Jupyter Notebooks 中的无标签输出引起的。输出现在在渲染之前已经过正确的审查。此漏洞被标记为 CVE-2017-0923。

受影响版本

GitLab CE and EE 8.4.0 - 9.5.10

GitLab CE and EE 10.0.0 - 10.1.5

GitLab CE and EE 10.2.0 - 10.2.5

GitLab CE and EE 10.3.0 - 10.3.3