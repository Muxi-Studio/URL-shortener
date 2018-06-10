from . import api
from flask_restful import Resource,abort,reqparse,Api
from app.models import db,URLMapping
from .authentication import auth
from app.decorators import moderator_required,admin_required
from utils import transform

api=Api(api,prefix="/urlmap")

parser = reqparse.RequestParser()

#parser是post请求的参数要求
parser.add_argument('long_url', type=str, required=True,help="原始长url")
parser.add_argument('custom_short_code',type=str,help="用户自定义短码，可选参数")

#parser_copy是put请求的参数要求
parser_copy=parser.copy()
parser_copy.remove_argument("custom_short_code")
parser_copy.replace_argument('long_url', type=str, required=True,help="需要更改成的目标长url")

class URLMapHandlerClass(Resource):

    def get(self,id):
        url_map=URLMapping.Query.get_or_404(id)
        return url_map.to_json(),200

    @auth.login_required
    def post(self,id):
        args=parser.parse_args(strict=True)
        short_code=args["custom_short_code"]
        long_url=args["long_url"]
        urlmap=URLMapping.query.filter_by(long_url=long_url).first()
        if urlmap:#长url已经存在,此时如果自定义了短码则忽略
            return urlmap.to_json(),200
        else:#long_url不存在
            if short_code:#用户自定义了短码
                urlmap=URLMapping.query.filter_by(short_code=short_code).first()
                if urlmap:#短码存在
                    return {"msg":"short_code {} already exist".format(short_code)},202
                else:#短码不存在
                    um=URLMapping(long_url=long_url,short_code=short_code,
                               item_type="user-defined",id_used=False,user_id=g.current_user.id)
                    db.session.add(um)
                    db.session.commit()
                    return um.to_json(),200
            else:#long_url不存在，用户未自定义短码
                custom_um = URLMapping.query.filter_by(id_used=False).first()
                if custom_um:
                    real_short_code=transform(custom_um.id)
                    um = URLMapping(long_url=long_url,short_code=real_short_code,
                                 id_used=False,user_id=g.current_user.id)
                    custom_um.id_used=True
                    db.session.add_all([um,custom_um])
                    db.session.commit()
                    return um.to_json(),200
                else:
                    um=URLMapping(long_url=long_url,short_code="placeholder",id_used=True,user_id=g.current_user.id)
                    db.session.add(um)
                    db.session.commit()
                    um.short_code=transform(um.id)
                    db.session.add(um)
                    db.session.commit()
                    return um.to_json(),200

    @auth.login_required
    def delete(self,id):
        um=URLMapping.query.get_or_404(id)
        if (g.current_user.id==3) or (g.current_user.id==um.user_id):
            db.session.delete(um)
            db.session.commit()
            return {"msg":'urlmapping deleted'},200
        else:
            return {"msg":"你无权删除该资源"},403


    @auth.login_required
    def put(self,id):
        um = URLMapping.query.get_or_404(id)
        if (g.current_user.id == 2) or (g.current_user.id == um.user_id):
            args=parser_copy.parse_args(strict=True)
            target=args['long_url']
            if URLMapping.query.filter_by(long_url=target).first() is not None:
                return {"msg":"更新的目标url已经存在"},202
            um=URLMapping.query.get_or_404(id)
            um.long_url=target
            db.session.add(um)
            db.session.commit()
            return {"msg":"URLMapping updated"},200
        else:
            return {"msg": "你无权更改该资源"}, 403

api.add_resource(URLMapHandlerClass, '/<int:id>/',endpoint="URLmap")
