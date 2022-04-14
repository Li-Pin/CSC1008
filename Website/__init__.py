from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Setting up database
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'thisisaverysecretivekey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, drivertble
    create_database(app)

    @login_manager.user_loader
    def load_user(user_id):
        value = session['databaseValue']
        if value == 1:
            return User.query.get(int(user_id))
        elif value == 2:
            return drivertble.query.get(int(user_id))


    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    return app


# check whether database exists
def create_database(app):
    if not path.exists('Website/' + DB_NAME):
        db.create_all(app=app)
