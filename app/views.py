# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from flask import render_template, request

from blog import app


@app.route('/')
def homepage():
    name = request.args.get('name')
    number = request.args.get('number')
    return render_template('homepage.html', name=name, number=number)
