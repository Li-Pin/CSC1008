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
    onRide = db.Column(db.String(80))
    journeyRoute = db.Column(db.String(80))


# driver database
class drivertble(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    carplate = db.Column(db.String(80))
    isAvailable = db.Column(db.String(80))
    journeyRoute = db.Column(db.String(80))
    driverloc = db.Column(db.String(80))
