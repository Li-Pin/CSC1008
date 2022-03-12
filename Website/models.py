from . import db
from flask_login import UserMixin
from sqlalchemy import func


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    rides = db.relationship('Rides')

class Rides(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fromLocation = db.Column(db.Float(100))
    toLocation = db.Column(db.Float(100))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
