# coding: utf-8
"""
    paginate.py
    ```````````
    : 分页api
"""
from flask import url_for


def pagination(lit, page, perpage,endpoint):
    """
    返回当前分页的列表对象,
    next、last链接
    {current: next_lit}
    """
    _yu = len(lit) % perpage
    _chu = len(lit) // perpage
    if _yu == 0:
        last = _chu
    else:
        last = _chu + 1
    current = lit[perpage*(page-1): perpage*page]
    next_page = ""
    if page < last:
        next_page = url_for(endpoint, page=page+1)
    elif page == last:
        next_page = ""
    last_page = url_for(endpoint, page=last)
    return [current, (next_page, last_page)]
