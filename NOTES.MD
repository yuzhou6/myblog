export MAIL_SENDER=lucat369@qq.com &&
export ZHIHU_ADMIN=lucat369@qq.com &&
export MAIL_USERNAME=lucat369@qq.com &&
export MAIL_PASSWORD=htxqjfrsvmkvdffc &&
export DATABASE_URL=mysql://root:1234@localhost/myblog &&
export ZHIHU_CONFIG=production

CREATE DATABASE myblog
CHARACTER SET 'utf8'
COLLATE 'utf8_general_ci';

> 知乎笔记

    蓝图注册在 __init__ 中
   
> 问题笔记汇总

1. app.app_context()
2. return response
3. os.path.abspath(os.path.dirname())
4. 文件夹app 下的 __init__.py 中的 app =  Flask(__name__) 这个 __name__ 具体是指什么
5. models.py 文件夹中的 Index = True
6. db.relationship('User', backref='role', lazy='dynamic') 中的 backref = 'role' 是表名还是类名
7. request.args.get('next') 是什么意思
8. Flask-Login 要求程序实现一个回调函数
    ```python    
    @login_manager.user_load_user()
        def load_user(user_id):
            return User.query.get(int(user_id))
            
9. python manage.py db migrate 改变不了字段长度
10. 修改字段长度 alter table user modify column name varchar(50) ;
11. backref='post', lazy='dynamic' 是什么意思
12. $('').attr('value','') 设置 textarea 的值不得行， 用 $('').val('这里是你的值') 才得行 
13. 比较奇怪的地方 author = current_user._get_current_object()
14. - def __repr__(self):
        return " %s" % self.category     # 这句话也是搞笑

-----
   
    报错汇总
   
1. Importing flask.ext.script is deprecated, use flask_script instead.
    - Use the 'flask_script' instead.
2. warnings.warn('SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and w
    - SQLALCHEMY_TRACK_MODIFICATIONS = False
3. sqlalchemy.exc.OperationalError: (_mysql_exceptions.OperationalError) (1049, "U)
    - 数据库 zhihu 没创建，知乎需要手动创建
4. pycharm的HTML代码写 {% 的时候 不能自动补全 , render_template() 不会补全
    - 在 PyCharm中File>Settings>Languages&Frameworks>Python Template Languages中，选择合适的模板语言。
    - 在 PyCharm中File>Settings>Project zhihu 中 点击创建有的 templates 右键，选中 templates, 然后该文件夹就变紫，有智能提示了
5. 撤销某个文件的提交 
    - git reset --HEAD <文件名>
6. 使用 "bootstrap/base.html" 出现 Internal Server Error 500 错误
    - 在 {% blcok navbar %} 中是使用了 
7. python manager.py db migrate 出现问题 alembic.util.exc.CommandError: Can't locate revision identified by '852aaf394ee6'
    - 进入数据库 use zhihu 接着 DROP TABLE alembic_version;
8. mysqk 修改字段 alter table test change t_name t_name_new varchar(20);

9. 明天加渐变属性

---

1. 踩的坑 
    - 登录需要 login_required 的， 先得 login_user(user) 
    - python
    -     if form.validate_on_submit and session['code'] == form.validate_code.data:
            要是一个 form.validate_on_submit 就得加括号 form.validate_on_submit()
    - 多表查询 
    -        u = User.query.filter(or_(User.username == 'we1i', User.phone == '18166384184')).first()
    - 使用 {{ form.password() }} 得 加上  {{ form.csrf_token() }}
    - url_for 接的是 视图路由 render_template 接的是 模板下的网页

2. 在 Class Role 中
    - 这么一句话     users = db.relationship('User', backref='role', lazy='dynamic') 表示引引接到 User 表中，只要 User 表的对象
    举个例子， u = User.query.filter_by(username = 'wei').first() 得奥一个 User类的对象 u.role 那么就会得到之前的 根据 role_id 这个在 User 类外键中的 Role 的所有信息
    说白了， 先在 User 类中建立一个外键， 生命连到 Role ,接着在 Role 里面，特有的 声明歌 User 类同过这个方法，可用之间调用 Role 类属性的东西
    users = db.relationship('User', backref='role', lazy='dynamic') 这个就应运而生了
    - 而反过来， 在 Role 表中，我们只要通过 r = Role.query.filter_by(name = 'Administator').first()
    那么 这个 r 就是所有的， 属性name 为 "Administrator" 的 User 集合，这是一个集合，所以想取得其中的每一歌个值，我们得遍历
    for u in r.users:
        print u.phone 
        
3. - 数据库需要真正的用户对象,因此要调用 _get_current_object() 方法
   
   
   
 
    

 
    
    