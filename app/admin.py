# -*- coding: utf-8 -*- 
__author__ = 'jwh5566'

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from blog import app, db
from models import Entry, Tag, User


admin = Admin(app, 'Blog Admin')
admin.add_view(ModelView(Entry, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(User, db.session))