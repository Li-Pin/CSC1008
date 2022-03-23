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


# user database
class TEST_ride(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pickUp = db.Column(db.String(80))
    dropOff = db.Column(db.String(80))
    date = db.Column(db.String(100))
    time = db.Column(db.String(80))
    pax = db.Column(db.String(80))
    carType = db.Column(db.String(80))


# Book shared ride database
class table2(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #pickUp = db.Column(db.String(80))
    #secondPickup = db.Column(db.String(80))
    #dropOff = db.Column(db.String(80))
    #secondDropoff = db.Column(db.String(80))
    #date = db.Column(db.String(100))
    #time = db.Column(db.String(80))
    pax = db.Column(db.String(80))
    #paym=db.column(db.String(100))


# Payment = db.column(db.String(100))


# rides database
class Rides(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fromLocation = db.Column(db.Float(100))
    toLocation = db.Column(db.Float(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
