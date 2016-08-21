#coding:utf-8
#!/usr/bin/env python
import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Role

app = create_app(os.environ.get('ZHIHU_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)      #在 app文件夹下引入 db ，在这用 migrate 控制

def make_shell_context():
    return dict(app = app , db = db, User = User, Role = Role )

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()