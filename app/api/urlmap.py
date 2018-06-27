#coding: utf-8

"""
urlmap.py 长url与短码之间的映射关系管理API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(GET) /api/user/<int:id>/urlmaps/ 获取某一用户的所有urlmap信息,
                                协管员以上权限或获取当前用户的urlmap信息。
(GET) /api/urlmap/<int:id>/ 获取某一id的url映射的信息
(POST)　/api/urlmap/0/ 创建一个url映射，需登录
(PUT)　/api/urlmap/<int:id>/ 更新一个urlmap,需要协管员以上权限或者该urlmap的创建者
(DELETE)　/api/urlmap/<int:id>/ 删除某一url映射，需要管理员权限或者是该urlmap的创建者
"""


from . import api
from flask import jsonify,g
from datetime import datetime
from flask_restful import Resource, abort, reqparse, Api
from app.models import db, URLMapping,Permission,User
from .authentication import auth
from utils import transform
from app.decorators import confirmed_required

@auth.login_required
@confirmed_required
@api.route("/user/<int:id>/urlmaps/",methods=['GET'])
def get_urlmaps_by_userID(id):
    u=User.query.get_or_404(id)
    if (g.current_user.can(Permission.MODERATE_COMMENTS)) or (g.current_user.id == id):
        urlmaps=u.urlmaps.all()
        return jsonify([urlmap.to_json() for urlmap in urlmaps]),200
    else:
        return jsonify({"msg":"权限不够"}),403


api = Api(api, prefix="/urlmap")

parser = reqparse.RequestParser()

# parser是post请求的参数要求
parser.add_argument('long_url', type=str, required=True, help="原始长url")
parser.add_argument('custom_short_code', type=str, help="用户自定义短码，可选参数")

# parser_copy是put请求的参数要求
parser_copy = parser.copy()
parser_copy.remove_argument("custom_short_code")
parser_copy.replace_argument('long_url', type=str,
                             required=False, help="需要更改成的目标长url")
parser_copy.add_argument("password",type=str,required=False,help="需要设置的密码")
parser_copy.add_argument('lock',type=bool,required=False,help="上锁和取消锁")


class URLMapHandlerClass(Resource):

    @auth.login_required
    @confirmed_required
    def get(self, id):
        url_map = URLMapping.query.get_or_404(id)
        return url_map.to_json(), 200

    @auth.login_required
    @confirmed_required
    def post(self, id):
        args = parser.parse_args(strict=True)
        short_code = args["custom_short_code"]
        long_url = args["long_url"]
        urlmap = URLMapping.query.filter_by(long_url=long_url).first()
        if urlmap:  # 长url已经存在,此时如果自定义了短码则忽略
            return urlmap.to_json(), 200
        else:  # long_url不存在
            if short_code:  # 用户自定义了短码
                urlmap = URLMapping.query.filter_by(short_code=short_code).first()
                if urlmap:  # 短码存在
                    return {"msg": "short_code {} already exist".format(short_code)}, 202
                else:  # 短码不存在
                    um = URLMapping(long_url=long_url, short_code=short_code,
                                    item_type="user-defined", id_used=False,
                                    user_id=g.current_user.id)
                    db.session.add(um)
                    db.session.commit()
                    return um.to_json(), 200
            else:  # long_url不存在，用户未自定义短码
                custom_um = URLMapping.query.filter_by(id_used=False).first()
                if custom_um:
                    real_short_code = transform(custom_um.id)
                    um = URLMapping(long_url=long_url, short_code=real_short_code,
                                    id_used=False, user_id=g.current_user.id)
                    custom_um.id_used = True
                    db.session.add_all([um, custom_um])
                    db.session.commit()
                    return um.to_json(), 200
                else:
                    um = URLMapping(long_url=long_url, short_code="placeholder", id_used=True,
                                    user_id=g.current_user.id)
                    db.session.add(um)
                    db.session.commit()
                    um.short_code = transform(um.id)
                    db.session.add(um)
                    db.session.commit()
                    return um.to_json(), 200


    @auth.login_required
    @confirmed_required
    def delete(self, id):
        um = URLMapping.query.get_or_404(id)
        if (g.current_user.is_administrator()) or (g.current_user.id == um.user_id):
            db.session.delete(um)
            db.session.commit()
            return {"msg": 'urlmapping deleted'}, 200
        else:
            return {"msg": "你无权删除该资源"}, 403


    @auth.login_required
    @confirmed_required
    def put(self, id):
        um = URLMapping.query.get_or_404(id)
        if (g.current_user.can(Permission.MODERATE_COMMENTS)) or (g.current_user.id == um.user_id):
            args = parser_copy.parse_args(strict=True)
            long_url = args['long_url']
            password=args['password']
            lock=args['lock']
            if long_url is not None:
                if URLMapping.query.filter_by(long_url=long_url).first() is not None:
                    return {"msg": "更新的目标url已经存在"}, 202
                um.long_url = long_url
            if password is not None:
                um.password=password
            if lock is not None:
                um.is_locked=lock
            um.update_time=datetime.utcnow()
            db.session.add(um)
            db.session.commit()
            return {"msg": "URLMapping updated"}, 200
        else:
            return {"msg": "你无权更改该资源"}, 403


api.add_resource(URLMapHandlerClass, '/<int:id>/', endpoint="URLmap")
