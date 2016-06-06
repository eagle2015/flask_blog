# -*- coding: utf-8 -*- 
__author__ = 'jwh5566'

from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from blog import app, db
from models import Entry, Tag, User
from wtforms.fields import SelectField, PasswordField
from flask_admin.contrib.fileadmin import FileAdmin
from flask import g, url_for, redirect, request

class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (g.user.is_authenticated and g.user.is_admin()):
            return redirect(url_for('login', next=request.path))
        return self.render('admin/index.html')

class AdminAuthentication(object):
    def is_accessible(self):
        return g.user.is_authenticated and g.user.is_admin()

class BaseModeView(AdminAuthentication, ModelView):
    pass

class SlugModeView(BaseModeView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(SlugModeView, self).on_model_change(form, model, is_created)


class EntryModeView(SlugModeView):
    _status_choices = [(choice, label) for choice, label in [
        (Entry.STATUS_PUBLIC, 'Public'),
        (Entry.STATUS_DRAFT, 'Draft'),
        (Entry.STATUS_DELETED, 'Deleted'),
    ]]
    #
    form_args = {
        'status': {'choices': _status_choices, 'coerce': int},
    }
    #
    form_columns = ['title', 'body', 'status', 'author', 'tags']
    form_overrides = {'status': SelectField}
    form_ajax_refs = {
        'author':{
            'fields': (User.name, User.email),
        }
    }



    column_choices = {'status': _status_choices,}

    column_filters = [
        'status', User.name, User.email, 'created_timestamp'
    ]

    column_list = [
        'title', 'status', 'author', 'tease', 'tag_list', 'created_timestamp',
    ]
    column_searchable_list = ['title', 'body']
    column_select_related_list = ['author']


class UserModeView(SlugModeView):
    column_filters = ('email', 'name', 'active', 'admin')
    column_list = ['email', 'name', 'active', 'created_timestamp', 'admin']
    column_searchable_list = ['email', 'name']

    form_columns = ['email', 'password', 'name', 'active', 'admin']
    form_extra_fields = {
        'password': PasswordField('New password'),
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = User.make_password(form.password.data)
        return super(UserModeView, self).on_model_change(form, model, is_created)

class BlogFileAdmin(AdminAuthentication, FileAdmin):
    pass



admin = Admin(app, 'Blog Admin', index_view=IndexView())
admin.add_view(EntryModeView(Entry, db.session))
admin.add_view(SlugModeView(Tag, db.session))
admin.add_view(UserModeView(User, db.session))
admin.add_view(
    BlogFileAdmin(app.config['STATIC_DIR'], '/static/', name='Static Files')
)