from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    return render_template("login.html")


@auth.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')                     # Set the value of the field username
        password = request.form.get('password')                   # Set the value of the field password1
        email = request.form.get('email')                   # Set the value of the field password2

        new_user = User(username=username, password=password, email=email)                            # Store input data into an object new_user
        db.session.add(new_user)                                    # Add the data into the db session
        db.session.commit()                                         # Commit the changes

    return render_template("register.html")