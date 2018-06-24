#coding: utf-8

"""
jump.py 跳转并统计
~~~~~~~~~~~~~~~~~~

GET /<short_code>/ 跳转并统计

由于本系统包含数据统计功能，所以这里使用的是302重定向(临时重定向)
"""
from . import app,db
from .models import URLMapping,Statistics
from flask import redirect,request,abort

@app.route('/<short_code>/',methods=['GET'])
def jump(short_code):
    urlmap=URLMapping.query.filter_by(short_code=short_code).first()
    if not urlmap:
        abort(404)
    urlmap.count+=1
    remote_ip=request.remote_addr
    user_agent=request.headers.get("User-Agent")
    s=Statistics(ip=remote_ip,useragent=user_agent,urlmap_id=urlmap.id)
    db.session.add_all([s,urlmap])
    db.session.commit()
    return redirect(urlmap.long_url,302,"正在跳转...")

