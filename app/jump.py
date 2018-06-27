#coding: utf-8

"""
jump.py 跳转并统计
~~~~~~~~~~~~~~~~~~

GET /<short_code>/ 跳转并统计
    如果该短码对应的url映射已上锁，则不予以跳转
    如果该段码对应的url映射设有密码，则跳转值通信页面，填入正确密码之后方可跳转成功
    如果该url既没有上锁，也没有设置密码，则正常跳转值短码对应的长url

由于本系统包含数据统计功能，所以这里使用的是302重定向(临时重定向)
"""
from . import app,db
from .forms import Form
from datetime import datetime
from .models import URLMapping,Statistics
from flask import redirect,request,abort,\
    jsonify,url_for,render_template

@app.route('/<string:short_code>',methods=['GET'])
def jump(short_code):
    urlmap=URLMapping.query.filter_by(short_code=short_code).first()
    if not urlmap:
        abort(404)
    urlmap.count+=1
    urlmap.last_click_time=datetime.utcnow()
    remote_ip=request.remote_addr
    user_agent=request.headers.get("User-Agent")
    s=Statistics(ip=remote_ip,useragent=user_agent,urlmap_id=urlmap.id)
    db.session.add_all([s,urlmap])
    db.session.commit()
    if urlmap.is_locked:
        return jsonify({"msg":"this url map is locked!","owner_email":urlmap.user.email}),503
    elif urlmap.password_hash is not None:
        return  redirect(url_for("need_pwd",id=urlmap.id),302)
    return redirect(urlmap.long_url,302)

@app.route('/password/',methods=['GET','POST'])
def need_pwd():
    urlmap_id = request.args.get('id')
    form = Form()
    urlmap=URLMapping.query.get_or_404(urlmap_id)
    if request.method=='GET':
        return render_template('password.html',form=form,urlmap_id=urlmap_id,email=urlmap.user.email)
    elif form.validate_on_submit():
        password=form.password.data
        urlmap=URLMapping.query.get_or_404(urlmap_id)
        if urlmap.verify_password(password):
            return redirect(urlmap.long_url,302)
        return jsonify({"msg":"password is invalid"}),401


