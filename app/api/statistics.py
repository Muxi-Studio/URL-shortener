# coding: utf-8

"""
statistics.py URLmap的统计信息


"""

import json
from . import api
from flask import jsonify,request
from utils import pagination
from .authentication import auth
from app.models import URLMapping,Statistics
from app.decorators import moderator_required,confirmed_required

@auth.login_required
@confirmed_required
@api.route("/urlmap/<int:id>/statistics/",methods=['GET'])
def get_statistics_by_urlmapID(id):
    urlmap=URLMapping.query.get_or_404(id)
    statistics=urlmap.statistics.all()
    return jsonify({"data":[s.to_json() for s in statistics]})


@moderator_required
@confirmed_required
@api.route('/statistics/',methods=['GET'])
def get_all_statistics():
    page = request.args.get('page', 1, type=int) or '1'
    per_page = request.args.get('per_page', type=int) or '20'
    statistics=Statistics.query.all()
    pagination_lit=pagination(statistics,int(page),int(per_page),"api.get_all_statistics")
    current = pagination_lit[0]
    next_page = pagination_lit[1][0]
    last_page = pagination_lit[1][1]
    return json.dumps(
        [s.to_json() for s in current],
        ensure_ascii=False,
        indent=1
    ), 200, {'link': '<%s>; rel="next", <%s>; rel="last"' %
                     (next_page, last_page)}

