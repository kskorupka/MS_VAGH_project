from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    '''
    A class used to represent User Table

    Attributes
    ----------
    id : int
        User's id in DataBase
    email : str
        unique User's email
    password : str
        User's password (length must be greater than 7 and contains at least one number)
    name : str
        User's name (cannot contain any number)
    surname : str
        User's surname (cannot contain any number)
    phone : str
        User's phone number (length must be 9 and cannot contain any letter)
    '''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    phone = db.Column(db.String(150))


class History(db.Model):
    '''
    A class used to represent History Table

    Attributes
    ----------
    historyID : int

    userID : int

    locationID : int

    itemID : int

    fromDate : DateTime

    toDate : DateTime

    '''
    historyID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    locationID = db.Column(db.Integer, db.ForeignKey('location.locationID'))
    itemID = db.Column(db.Integer, db.ForeignKey('item.itemID'))
    fromDate = db.Column(db.DateTime(timezone=True))
    toDate = db.Column(db.DateTime(timezone=True))


class Location(db.Model):
    locationID = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    nearTo = db.Column(db.String)
    name = db.Column(db.String)


class Reservation(db.Model):
    reservationID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    itemID = db.Column(db.Integer, db.ForeignKey('item.itemID'))
    fromDate = db.Column(db.DateTime(timezone=True))


class Item(db.Model):
    itemID = db.Column(db.Integer, primary_key=True)
    locationID = db.Column(db.Integer, db.ForeignKey('location.locationID'))
    type = db.Column(db.String)
    weight = db.Column(db.Float)
    color = db.Column(db.String)


class Damaged(db.Model):
    damageID = db.Column(db.Integer, primary_key=True)
    itemID = db.Column(db.Integer, db.ForeignKey('item.itemID'))
    type = db.Column(db.String)
    fromDate = db.Column(db.DateTime(timezone=True))
    toDate = db.Column(db.DateTime(timezone=True))
    repairing = db.Column(db.Boolean)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    phone = db.Column(db.String(150))


class Announcement(db.Model):
    announcementID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)


class Report(db.Model):
    reportID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String)
