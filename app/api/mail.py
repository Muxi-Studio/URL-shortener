# coding: utf-8
# from app import celery
# from flask import render_template
# from flask_mail import Message
# from app import app, mails
#
#
# def msg_dict(to, user, token, **kwargs):
#     """
#     生成邮件
#     """
#     msg = Message(
#         subject='Muxi URL Shorter Service, please confirm you account!',
#         sender=app.config['MAIL_DEFAULT_SENDER'] or '3480437308@qq.com',
#         recipients=[to]
#     )
#     msg.body = render_template('templates/confirm.txt', user=user, token=token, **kwargs)
#     msg.html = render_template('templates/confirm.html', user=user, token=token, **kwargs)
#     return msg.__dict__
#
#
# @celery.task
# def send_async_email(msg_dict):
#     with app.app_context():
#         msg = Message()
#         msg.__dict__.update(msg_dict)
#         mails.send(msg)
#
#
# def send_mail(to, user, token, **kwargs):
#     """
#     发送邮件
#     """
#     send_async_email.delay(msg_dict(to, user, token ** kwargs))


from threading import Thread
from app import app
from flask_mail import Mail,Message
from flask import render_template

mail=Mail(app)


def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to,template,**kwargs):
    msg=Message("Confirm you account",sender='3480437308@qq.com',recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)
    thr=Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr

