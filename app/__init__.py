#coding: utf-8

import os

from celery import Celery
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import config

db=SQLAlchemy()

#工厂函数
def create_app(config_key):
    app=Flask(__name__)
    app.config.from_object(config[config_key])

    config[config_key].init_app(app)
    db.init_app(app)

    #注册蓝图
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app

#the project app
app = create_app(config_key = os.getenv('APP_CONFIG') or 'default')
mails=Mail(app)



def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URI'],
                    backend=app.config["CELERY_BACKEND_URI"])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery_app=make_celery(app)




from . import jump

#注意，这里一定需要导入，不然就会出现未注册的task
from .tasks import send_mail
