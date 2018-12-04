# 启动flask程序脚本

from app import creat_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Role
from app.spider.dianying_spider import add_movie
# from app.spider.dianying_spider_asyncio import add_movie


app = creat_app('default')
manager = Manager(app)
migrate = Migrate(app, db=db)


def make_shell_context():
    return dict(app=app, User=User, Role=Role)


# 添加shell命令，增加shell上下文
manager.add_command('shell', Shell(make_context=make_shell_context))
# MigrateCommand命令添加的shell的db命令中
manager.add_command('db', MigrateCommand)
# 增加runserver命令
# manager.add_command('runserver', Server(
#     use_debugger=True,
#     use_reloader=True,
#     host='0.0.0.0',
#     port='5000'
# ))


# 增加电影命令，add_movie
@manager.command
def add_movies():
    add_movie()


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import User, Role

    # 把数据库迁移到最新修订版本
    upgrade()

    # 创建用户角色
    Role.insert_roles()


if __name__ == '__main__':
    manager.run()





