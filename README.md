# MyBlog

## 项目介绍

该博客使用 Python 的 Flask 框架搭建，可部署在 SAE 或者 VPS 上。

演示地址为：http://oldblog.applinzi.com/ 

编写文章的编辑器使用 Markdown 编辑器，非常适合程序猿写博客。

## 部署准备工作

域名: 阿里云购买，购买后进行域名解析，指向自己的 VPS 的服务器即可

主机 VPS 购买：https://www.vultr.com/

安装的系统：Ubuntu-14.04.4 x64

### (1) 升级 Python 版本

**由于 Ubuntu-14.04.4 x64 自带的 Vim, Python, Git 版本过低，所以进行下升级**
> **升级 Python**

**版本`Python2.7.6` 升级到最新 `Python2.7.12` 执行以下命令：**

```
 sudo add-apt-repository ppa:fkrull/deadsnakes-python2.7  
 sudo apt-get update  
 sudo apt-get upgrade  
```

### (2) 升级 Git 版本

**执行以下命令：**

```
sudo add-apt-repository ppa:git-core/ppa
sudo apt-get update
sudo 
```

### (3) 升级 Vim 版本

```
sudo add-apt-repository ppa:nmi/vim-snapshots  
sudo apt-get update  
sudo apt-get install vim  
```

**好了，版本升级完后，可以开始安装一些必备东西了，下面我将一步步写出来**

**需要用到的东西`Nginx`（用以代理） `MySQL`(数据库) `gunicorn `（产生服务器） `supervisor`（为了退出终端时，你的程序还能继续运行）**

### (4) 新建用户

**新建用户 登录后，以 root 的身份，新建一个非管理员用户**

```
# 创建新用户，名字可个人喜好，我这里为zhou
$ useradd zhou -m -s /bin/bash

# 设置新用户密码
$ passwd zhou

# 为新用户添加sudo
$ adduser zhou sudo

# 切换到新的用户
$ su zhou
```
### (5) 安装 `Virtualenv` 虚拟环境管理

```
sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install virtualenv
```
### (6) 安装 `Nginx` 

```
sudo add-apt-repository ppa:nginx/stable
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install build-essential python python-dev
sudo apt-get install nginx
```
### (7) 创建项目目录

**(重要)还要设置目录所属用户和用户组为当前用户**

```
sudo mkdir /home/www && cd /home
sudo chown -R zhou:zhou www && cd www
```

### (8) 下载源码

```
git clone https://github.com/yuzhou6/myblog
```

### (9) 创建虚拟环境

```
virtualenv venv
source venv/bin/activate
```


### (10) 安装 `gunicorn`

```
(venv) $ pip install -r requirements/dev.txt
(venv) $ pip install gunicorn
```
### (11) 配置 `MySQL` 

```
(venv) $ sudo apt-get install mysql-server python-mysqldb libmysqlclient-dev
(venv) $ pip install mysql-python
```
**（重要）安装完后 root 用户登录 MySQL 并创建数据库 : myblog （数据库名自己定）**

```
(venv) $ mysql -u root -p
mysql> CREATE DATABASE myblog
       CHARACTER SET 'utf8'
       COLLATE 'utf8_general_ci';
mysql> exit
```

**其中，设置`CHARACTER SET 'utf8'`和`COLLATE 'utf8_general_ci'`是为了防止中文乱码**。

### (12) 配置 `Nginx` 环境

```
(venv) $ sudo /etc/init.d/nginx restart
(venv) $ sudo rm /etc/nginx/sites-enabled/default
(venv) $ sudo touch /etc/nginx/sites-available/myblog
(venv) $ sudo ln -s /etc/nginx/sites-available/myblog /etc/nginx/sites-enabled/myblog
```
### （13） 编辑 `Nginx` 项目文件

```
(venv) $ sudo vim /etc/nginx/sites-enabled/myblog
```

**添加如下内容**

```
server {
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /static {
        alias  /home/www/myblog/app/static/;
    }
}
```

### (14) 重启 `Nginx` 

```
(venv) $ sudo /etc/init.d/nginx restart
```
### (15) 将角色写入数据库

**将角色写入数据库**

```
(venv) $ python manage.py shell
>>> db.create_all()
>>> Role.insert_roles()
>>> Category.insert_categorys()
>>> exit()
```
### (15) 启动博客

```
(venv) $ cd /home/www/myblog/
(venv) $ gunicorn manage:app -b localhost:8000
```
**那么，现在可以由 `域名` 或者你的 `VPS 的 IP 地址`访问网站了**

**光这样还不行，我们还得进行最后一步，退出终端后，网站还不能继续运行**

### (16) 安装 `supervisor` 用以启动 `gunicorn`

```
(venv) $ pip install supervisor
(venv) $ echo_supervisord_conf > supervisor.conf  # 生成supervisor默认配置文件
(venv) $ vim supervisor.conf                      # 修改supervisor配置文件，添加gunicorn进程管理 
```

**添加如下内容：**

```
[program:myblog]
command = gunicorn manage:app -b localhost:8000
directory = /home/www/myblog
autorestart = true
user = zhou
```

### (17) 成功在望，最后一个命令

```
(venv) $ supervisord -c supervisor.conf
```
**好了，可以关掉 shell 访问你的网站了要是存在什么问题，欢迎留言**
