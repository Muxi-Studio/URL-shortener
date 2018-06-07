from . import api
from flask_restful import Resource,abort,reqparse,Api

api=Api(api,prefix="/urlmap")

class URLMapHandlerClass(Resource):
    def get(self,id):
        return "hello,world"+str(id)

    def post(self,id):
        return "here is post"

    def delete(self,id):
        return "here is delete"

    def put(self,id):
        return "here is put"

api.add_resource(URLMapHandlerClass, '/<int:id>/',endpoint="URLmap")
