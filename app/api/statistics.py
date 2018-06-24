# coding: utf-8

"""
statistics.py URLmap的统计信息


"""
from . import api
from flask import jsonify
from .authentication import auth
from app.models import Permission,URLMapping,Statistics
from app.decorators import admin_required,permission_required,moderator_required

@auth.login_required
@api.route("/urlmap/<int:id>/statistics/",methods=['GET'])
def get_statistics_by_urlmapID(id):
    urlmap=URLMapping.query.get_or_404(id)
    statistics=urlmap.statistics.all()
    return jsonify([s.to_json() for s in statistics])

@moderator_required
@api.route('/statistics/',methods=['GET'])
def get_all_statistics():
    statistics=Statistics.query.all()
    return jsonify([s.to_json() for s in statistics])

