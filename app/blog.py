# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from flask import Flask, g
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import Configuration
from flask_bcrypt import Bcrypt
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
login_manager = LoginManager(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

@app.before_request
def _before_request():
    g.user = current_user

# @app.route('/')
# def homepage():
#     return 'bbbbbb'
#
# if __name__ == '__main__':
#     app.run()
