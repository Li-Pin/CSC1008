from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# Setting up database
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'thisisaverysecretivekey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .models import User
    create_database(app)

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    return app


# check whether database exists
def create_database(app):
    if not path.exists('Website/' + DB_NAME):
        db.create_all(app=app)
