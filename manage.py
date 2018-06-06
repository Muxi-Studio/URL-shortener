import os
from app import create_app,db
from flask_script import Manager,Shell
from app.models import Requirement,PingInfo
from flask_migrate import Migrate,MigrateCommand

app=create_app("default")
manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    """自动加载环境"""
    return dict(app=app,db=db,Requirement=Requirement,PingInfo=PingInfo)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command("db",MigrateCommand)

@manager.command
def command_360():
    pass
if __name__ == '__main__' :
manager.run()