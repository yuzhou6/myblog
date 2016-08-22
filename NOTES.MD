export MAIL_SENDER=lucat369@qq.com &&
export ZHIHU_ADMIN=lucat369@qq.com &&
export MAIL_USERNAME=lucat369@qq.com &&
export MAIL_PASSWORD=htxqjfrsvmkvdffc &&
export DATABASE_URL=mysql://root:1234@localhost/zhihu &&
export ZHIHU_CONFIG=production

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

---

1. 踩的坑 
    - 登录需要 login_required 的， 先得 login_user(user) 
    - python

 
    
    