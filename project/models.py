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

class Carts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    activestate = db.Column(db.String(100))
    


class CartItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer)
    #cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    #carts = db.relationship("Carts", backref = db.backref('cartitems', lazy=True))
    cart_id = db.Column(db.Integer)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    cartid = db.Column(db.Integer)
    status = db.Column(db.String(100))

class TransactionDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200))
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    transactions = db.relationship("Transactions", backref = db.backref('transactiondetails', lazy=True))
db.create_all(app=create_app())