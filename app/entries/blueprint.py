# -*- coding: utf-8 -*- 
__author__ = 'jwh5566'
from flask import Blueprint
from flask import render_template

from models import Entry
from helpers import object_List

entries = Blueprint('entries', __name__,
                    template_folder='templates')


@entries.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    return object_List('entries/index.html', entries)


@entries.route('/tags/')
def tag_index():
    pass


@entries.route('/tags/<slug>/')
def tag_detail(slug):
    pass


@entries.route('/<slug>/')
def detail(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    return render_template('entries/detail.html', entry=entry)
