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
        History's id in DataBase
    userID : int
        User's id in DataBase
    locationID : int
        Represents specified location in real world
    itemID : int
        Represents specified item like bike, board, or scooter
    fromDate : DateTime
        Date of loan
    toDate : DateTime
        Date of delivery
    '''
    historyID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    locationID = db.Column(db.Integer, db.ForeignKey('location.locationID'))
    itemID = db.Column(db.Integer, db.ForeignKey('item.itemID'))
    fromDate = db.Column(db.DateTime(timezone=True))
    toDate = db.Column(db.DateTime(timezone=True))


class Location(db.Model):
    '''
    A class used to represent Location Table

    Attributes
    ----------
    locationID : int
        Represents specified location in real world
    description : str
        Description of the surroundings of the point
    nearTo : str
        Famous facility nearby
    name : str
        This name is shown in application
    '''
    locationID = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    nearTo = db.Column(db.String)
    name = db.Column(db.String)


class Reservation(db.Model):
    '''
    A class used to represent Reservation Table

    Attributes
    ----------
    reservationID : int
        reservation's id in DataBase
    userID : int
        User's id in DataBase
    itemID : int
        Represents specified item like bike, board, or scooter
    fromDate : DateTime
        Date of loan
    '''
    reservationID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    itemID = db.Column(db.Integer, db.ForeignKey('item.itemID'))
    fromDate = db.Column(db.DateTime(timezone=True))


class Item(db.Model):
    '''
    A class used to represent Item Table

    Attributes
    ----------
    itemID : int
        Represents specified item like bike, board, or scooter
    locationID : int
        Represents specified location in real world
    type : str
        either bike, scooter or board
    weight : float
        Represents specified item weight
    color : str
        color of an item
    '''
    itemID = db.Column(db.Integer, primary_key=True)
    locationID = db.Column(db.Integer, db.ForeignKey('location.locationID'))
    type = db.Column(db.String)
    weight = db.Column(db.Float)
    color = db.Column(db.String)


class Damaged(db.Model):
    '''
    A class used to represent Damaged Table

    Attributes
    ----------
    damageID : int
        History's id in DataBase
    userID : int
        User's id in DataBase
    locationID : int
        Represents specified location in real world
    itemID : int
        Represents specified item like bike, board, or scooter
    fromDate : DateTime
        Date of loan
    toDate : DateTime
        Date of delivery
    '''
    damageID = db.Column(db.Integer, primary_key=True)
    itemID = db.Column(db.Integer, db.ForeignKey('item.itemID'))
    type = db.Column(db.String)
    fromDate = db.Column(db.DateTime(timezone=True))
    toDate = db.Column(db.DateTime(timezone=True))
    repairing = db.Column(db.Boolean)


class Admin(db.Model):
    '''
    A class used to represent Admin Table

    Attributes
    ----------
    id : int
        Admin id in DataBase
    email : str
        unique Admin email
    password : str
        Admin password (length must be greater than 7 and contains at least one number)
    name : str
        Admin name (cannot contain any number)
    surname : str
        Admin surname (cannot contain any number)
    phone : str
        Admin phone number (length must be 9 and cannot contain any letter)
    '''
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    phone = db.Column(db.String(150))


class Announcement(db.Model):
    '''
    A class used to represent Announcement Table

    Attributes
    ----------
    announcementID : int
        Announcement's id in DataBase
    title : str
        title of the announcement
    content : str
        content of the announcement
    '''
    announcementID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)


class Report(db.Model):
    '''
    A class used to represent Report Table

    Attributes
    ----------
    Report : int
        Report's id in DataBase
    userID : int
        User's id in DataBase
    description : str
        Description of existing report
    '''
    reportID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String)
