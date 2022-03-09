from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    return render_template("login.html")


@auth.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        print(username, password, email)

        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

    return render_template("register.html")