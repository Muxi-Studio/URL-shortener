from . import api
from app.models import Permission
from flask_restful import Resource,abort,reqparse,Api
from app.decorators import admin_required,permission_required

api=Api(api,prefix="/statistics")

class StatisticsHandlerClass(Resource):

    @permission_required(Permission.ADMINISTER)
    def get(self,id):
        return "hello,world"+str(id)

    def post(self,id):
        return "here is post"

    def delete(self,id):
        return "here is delete"

    def put(self,id):
        return "here is put"

api.add_resource(StatisticsHandlerClass, '/<int:id>/',endpoint="statistic")
