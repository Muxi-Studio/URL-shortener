from flask import Blueprint
api=Blueprint("api",__name__)

from . import long2short, statistics, urlmap, user,authentication