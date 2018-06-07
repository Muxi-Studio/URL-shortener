from . import api
from flask_restful import Resource,abort,reqparse,Api
from app.models import db,URLMapping

api=Api(api,prefix="/urlmap")

parser = reqparse.RequestParser()

#parser是post请求的参数要求
parser.add_argument('long_url', type=str, required=True,help="原始长url")
parser.add_argument('custom_short_code',type=str,help="用户自定义短码，可选参数")


class URLMapHandlerClass(Resource):
    def get(self,id):
        url_map=URLMapping.Query.get_or_404(id)
        return url_map.to_json()

    def post(self,id):
        return "here is post"

    def delete(self,id):
        return "here is delete"

    def put(self,id):
        return "here is put"

api.add_resource(URLMapHandlerClass, '/<int:id>/',endpoint="URLmap")
