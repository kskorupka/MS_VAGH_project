from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# creating schema
# additional class (just to test sqlalchemy functions)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # returns current time
    # adding foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # setting primary key
    email = db.Column(db.String(150), unique=True)  # each user has a unique email
    hasło = db.Column(db.String(150))
    imię = db.Column(db.String(150))
    nazwisko = db.Column(db.String(150))

# TODO: Add tables to your database (time: 1:29:10)
