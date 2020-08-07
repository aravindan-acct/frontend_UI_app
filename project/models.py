from . import db
from __main__ import create_app
from flask_login import UserMixin
'''
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    phone = db.Column(db.Integer)
'''
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000))

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tokenstring = db.Column(db.String(150))


db.create_all(app=create_app())