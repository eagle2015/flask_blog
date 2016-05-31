# -*- coding: utf-8 -*- 
__author__ = 'jwh5566'

from flask import render_template, request
from models import Entry


def object_List(template_name, query, paginate_by=20, **context):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    object_list = query.paginate(page, paginate_by)
    return render_template(template_name, object_list=object_list, **context)


def entry_List(template, query, **context):
    search = request.args.get('q')
    if search:
        query = query.filter(
            (Entry.body.contains(search)) |
            (Entry.title.contains(search))
        )
    return object_List(template, query, **context)
