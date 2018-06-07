"""
    manage.py
    ~~~~~~~~~
    : [intro]
    : -- xueer backend management
    : [shell]
      -- python manage.py db init
      -- python manage.py db migrate
      -- python manage.py db upgrade
      -- python manage.py runserver
      -- python manage.py test
      -- python manage.py adduser (username) (email)
      -- python manage.py freeze
"""

import os
from app import create_app,db
from flask_script import Manager,Shell
from app.models import Role,User,URLMapping,Statistics
from flask_migrate import Migrate,MigrateCommand

app=create_app("default")
manager=Manager(app)
migrate=Migrate(app,db)

def make_shell_context():
    """自动加载环境"""
    return dict(app=app,db=db,Role=Role,User=User,
                URLMapping=URLMapping,Statistics=Statistics)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command("db",MigrateCommand)



# api.add_resource(TodoList, '/todos')


if __name__ == '__main__' :
    manager.run()