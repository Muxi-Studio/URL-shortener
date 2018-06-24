#coding: utf-8

"""
user.py  用户资源的增删改查API
~~~~~~~~

(GET) /api/user/<int:id>/ 获取id用户的信息
(POST) /api/user/0/ 创建用户，此处的id为保持url一致而使用的占位符，
                            建议统一使用/api/user/0/
(PUT) /api/user/<int:id> 更新用户信息，需要协管员以上权限或者用户本人
(DELETE) /api/user/<int:id>/ 删除用户，需要管理员以上权限或者用户本人

"""


from . import api
from .authentication import auth
from app.decorators import admin_required,moderator_required
from flask_restful import Resource,reqparse,Api
from app.models import User,db,Permission
api=Api(api,prefix="/user")


parser = reqparse.RequestParser()
# parser是post请求中的参数要求
parser.add_argument('email', type=str, required=True,help="用户邮箱")
parser.add_argument('password',type=str,required=True,help="经过base64编码之后的用户密码")
parser.add_argument('role_id',type=int,help="用户角色")

#parser_copy是put请求中的参数要求
parser_copy = parser.copy()
parser_copy.replace_argument('email', type=str,help="用户新邮箱")
parser_copy.replace_argument('password',type=str,help="经过base64编码之后的新用户密码")


class UserHandlerClass(Resource):

    def get(self,id):
        u=User.query.get_or_404(id)
        return u.to_json(),200

    def post(self,id):
        args=parser.parse_args(strict=True)
        u=User(email=args["email"],password=args["password"],
             role_id=(args["role_id"] if args["role_id"] else 2))
        db.session.add(u)
        db.session.commit()
        return {"msg":"user created"},200

    @auth.login_required
    def delete(self,id):
        u=User.query.get_or_404(id)
        if (g.current_user.is_administrator()) or (g.current_user.id == u.id):
            db.session.delete(u)
            db.session.commit()
            return {"msg":"user deleted"},200
        else:
            return {"msg": "你无权删除该资源"}, 403

    @moderator_required
    def put(self,id):
        u = User.query.get_or_404(id)
        if (g.current_user.can(Permission.MODERATE_COMMENTS)) or (g.current_user.id == u.id):
            args = parser_copy.parse_args(strict=True)
            u.email=args["email"] if args["email"] else u.email
            if args["password"]:
                u.password=args["password"]
            db.session.add(u)
            db.session.commit()
            return {"msg":"user updated"},200
        else:
            return  {"msg": "你无权更改该资源"}, 403

api.add_resource(UserHandlerClass, '/<int:id>/',endpoint="user")
