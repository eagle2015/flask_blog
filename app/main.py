# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from app import app

from entries.blueprint import entries

app.register_blueprint(entries, url_prefix='/entries')

if __name__ == '__main__':
    app.run()