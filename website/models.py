from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Pass(db.Model):
    id_pass=db.Column(db.Integer,primary_key=True)
    price=db.Column(db.Integer)
    status=db.Column(db.String(150)) 
    date=db.Column(db.Date)  

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    age=db.Column(db.Integer)
    student=db.Column(db.String(150))
    donations = db.Column(db.Integer)
    id_pass=db.Column(db.Integer)
    member=db.Column(db.Boolean)
    notes = db.relationship('Note')

class Book(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    author=db.Column(db.String(150))
    name=db.Column(db.String(150))
    location=db.Column(db.String(150))
    status=db.Column(db.String(150))
    genre=db.Column(db.String(150))


class Rents(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    id_book=db.Column(db.Integer)
    id_user=db.Column(db.Integer)
    date=db.Column(db.Date)
    return_date=db.Column(db.Date)

class Location(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150))

 



    
