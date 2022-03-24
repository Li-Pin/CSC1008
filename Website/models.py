from . import db
from flask_login import UserMixin
from sqlalchemy import func
from datetime import datetime


# user database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    # rides = db.relationship('Rides')


# ride database
class TEST_ride(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pickUp = db.Column(db.String(80))
    dropOff = db.Column(db.String(80))
    date = db.Column(db.String(100))
    time = db.Column(db.String(80))
    pax = db.Column(db.String(80))
    carType = db.Column(db.String(80))
    paym = db.Column(db.String(80))


# shared ride database
class TEST_shared(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carType = db.Column(db.String(80))
    pickUp = db.Column(db.String(80))
    dropOff = db.Column(db.String(80))
    pax = db.Column(db.String(80))
    date = db.Column(db.String(80))
    time = db.Column(db.String(80))
    paym = db.Column(db.String(80))
