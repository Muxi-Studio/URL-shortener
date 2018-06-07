from . import api
from app.decorators import login_required
from flask import url_for
from flask_restful import Resource,abort,reqparse,Api

api=Api(api,prefix="/user")

class UserHandlerClass(Resource):

    @login_required
    def get(self,id):
        return url_for("api.URLmap",_external=True,id=1,_method="POST")

    def post(self,id):
        return "here is post"

    def delete(self,id):
        return "here is delete"

    def put(self,id):
        return "here is put"

api.add_resource(UserHandlerClass, '/<int:id>/',endpoint="user")
