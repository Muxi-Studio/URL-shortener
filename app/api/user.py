from . import api
from app.decorators import login_required,admin_required,moderator_required
from flask_restful import Resource,abort,reqparse,Api
from app.models import User,db
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
        return {},200

    @admin_required
    def delete(self,id):
        u=User.query.get_or_404(id)
        db.session.delete(u)
        db.session.commit()
        return {},200

    @moderator_required
    def put(self,id):
        u = User.query.get_or_404(id)
        args = parser_copy.parse_args(strict=True)
        u.email=args["email"] if args["email"] else u.email
        u.password=args["password"] if args["password"] else args["password"]
        db.session.add(u)
        db.session.commit()
        return {},200

api.add_resource(UserHandlerClass, '/<int:id>/',endpoint="user")
