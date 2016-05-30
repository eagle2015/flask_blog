# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# @app.route('/')
# def homepage():
#     return 'bbbbbb'
#
# if __name__ == '__main__':
#     app.run()
