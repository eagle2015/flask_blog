# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from blog import app
import views

from entries.blueprint import entries

app.register_blueprint(entries, url_prefix='/entries')

if __name__ == '__main__':
    app.run()