# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from app import app


@app.route('/')
def homepage():
    return 'Home page'