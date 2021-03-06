# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user
from blog import app, login_manager
from entries.forms import LoginForm

@app.route('/')
def homepage():
    name = request.args.get('name')
    number = request.args.get('number')
    return render_template('homepage.html', name=name, number=number)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            login_user(form.user, remember=form.remember_me.data)
            flash("successfully logged in as %s" % form.user.email, "success")
            return redirect(request.args.get("next")) or url_for("homepage")
    else:
        form = LoginForm()
        return render_template("login.html", form=form)

@app.route('/logout/')
def logout():
    logout_user()
    flash('you have been logged out.', 'success')
    return redirect(request.args.get('next')) or url_for('homepage')


