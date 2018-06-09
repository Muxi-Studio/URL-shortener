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
from app import app,db
from flask_script import Manager,Shell
from app.models import Role,User,URLMapping,Statistics
from flask_migrate import Migrate,MigrateCommand

manager=Manager(app)
migrate=Migrate(app,db)

COV = None
if os.environ.get('APP_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


def make_shell_context():
    """自动加载环境"""
    return dict(app=app,db=db,Role=Role,User=User,
                URLMapping=URLMapping,Statistics=Statistics)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command("db",MigrateCommand)


@manager.command
def test(coverage=True):
    """Run the unit tests."""
    import sys
    if coverage and not os.environ.get('APP_COVERAGE'):
        os.environ['APP_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.erase()
    sys.exit(0)





if __name__ == '__main__' :
    manager.run()