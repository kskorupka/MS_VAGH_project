from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    phone = db.Column(db.String(150))


class History(db.Model):
    historyID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    locationID = db.Column(db.Integer, db.ForeignKey('location.locationID'))
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


class Report(db.Model):
    reportID = db.Column(db.Integer, primary_key=True)
    report = db.Column(db.String)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    phone = db.Column(db.String(150))


class Announcement(db.Model):
    announcementID = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
