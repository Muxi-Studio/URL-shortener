#coding: utf-8
'''
tasks.py  celery异步任务
~~~~~~~~~~~~~~~~~~~~~~

启动命令:
    celery worker -A app.celery_app --loglevel=INFO

'''

from app import app
from flask_mail import Message
from app import mails
from flask import render_template
from app import celery_app


def msg_dict(to, user, token, **kwargs):
    """
    生成邮件
    """
    msg = Message(
        subject='Muxi URL Shorter Service, please confirm you account!',
        sender=app.config['MAIL_DEFAULT_SENDER'] or '3480437308@qq.com',
        recipients=[to]
    )
    msg.body = render_template('confirm.txt', user=user, token=token, **kwargs)
    msg.html = render_template('confirm.html', user=user, token=token, **kwargs)
    return msg.__dict__


@celery_app.task
def send_async_email(msg_dict):
    """
    异步发送邮件
    """
    with app.app_context():
        msg = Message()
        msg.__dict__.update(msg_dict)
        mails.send(msg)


def send_mail(to, user, token, **kwargs):
    """
    发送邮件
    """
    send_async_email.delay(msg_dict(to, user, token, **kwargs))


