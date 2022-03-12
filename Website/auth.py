from flask import render_template, url_for, request, Blueprint, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from . import db
from .models import User, Rides
from oneMapMethods import locationdet


auth = Blueprint('auth', __name__)


#Route to login page
@auth.route('/')
def login():
    return render_template('login.html')


@auth.route('/', methods=['GET', 'POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    #check if user exists
    #if user don't exist, prompt user to try again
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'danger')
        return redirect(url_for('auth.login'))
    # if user exists, log user in
    login_user(user)
    return redirect(url_for('auth.home'))


#Route to register page
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        #if it returns a user, there is already an existing user with the same email
        user = User.query.filter_by(email=email).first()

        #if there is an existing user, prompt user to try again
        if user:
            flash('Email address already exist, please use another email.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, password=generate_password_hash(password, method='sha256'), email=email)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration Success!', 'success')
        return redirect(url_for("auth.login"))

    return render_template("register.html")


#Route to homepage
@auth.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


#Route to book ride page
@auth.route('/bookride', methods=['GET', 'POST'])
def bookride():
    if request.method == 'POST':
        fromLocation = request.form.get('fromLocation') #Taking input from form
        toLocation = request.form.get('toLocation')
        fromLocation = locationdet(fromLocation) #Passing to API
        toLocation = locationdet(toLocation)
        fromLocationlat = fromLocation[0] #Assigning array values
        fromLocationlong = fromLocation[1]
        toLocationlat = toLocation[0]
        toLocationlong = toLocation[1]
        fromLocationname = fromLocation[2]
        toLocationname = toLocation [2]

        return redirect(url_for('auth.confirmride', fromLocationlat=fromLocationlat, fromLocationlong=fromLocationlong,
        toLocationlat=toLocationlat, toLocationlong=toLocationlong, fromLocationname=fromLocationname, toLocationname=toLocationname))

    return render_template("bookride.html")


@auth.route('/confirmride', methods=['GET', 'POST'])
def confirmride():
    fromLocationlat = request.args.get('fromLocationlat', None)
    fromLocationlong = request.args.get('fromLocationlong', None)
    toLocationlat = request.args.get('toLocationlat', None)
    toLocationlong = request.args.get('toLocationlong', None)
    fromLocationname = request.args.get('fromLocationname', None)
    toLocationname = request.args.get('toLocationname', None)

    return render_template("confirmride.html", fromLocationlat=fromLocationlat, fromLocationlong=fromLocationlong,
        toLocationlat=toLocationlat, toLocationlong=toLocationlong, fromLocationname=fromLocationname, toLocationname=toLocationname)


@auth.route('/settings')
def settings():
    return render_template("settings.html")
