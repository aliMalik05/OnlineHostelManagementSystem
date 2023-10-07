from .db import  db

class Admin(db.Document):
    email = db.StringField(required=True)
    password = db.StringField(required=True)

class StudentLogin(db.Document):
    name = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    status= db.StringField(required=True)
    email1 = db.StringField()

class Room(db.Document):
    roomNo = db.StringField(required=True)
    seator = db.StringField(required=True)
    roomRent = db.StringField(required=True)
    seatRent = db.StringField(required=True)
    livingStudents = db.StringField(required=True)
    remainingSeats = db.StringField(required=True)
    img = db.StringField(required=True)

class bookRequest(db.Document):
    sid = db.StringField(required=True)
    roomNo = db.StringField(required=True)
    name = db.StringField(required=True)
    email = db.StringField(required=True)
    paymentid = db.StringField(required=True)
    type = db.StringField(required=True)


class studentBooking(db.Document):
    roomNo = db.StringField(required=True)
    name = db.StringField(required=True)
    email = db.StringField(required=True)
    gname = db.StringField(required=True)
    gcontact = db.StringField(required=True)
    city = db.StringField(required=True)
    food = db.StringField(required=True)
    phone = db.StringField(required=True)
    cnic = db.StringField(required=True)
    country = db.StringField(required=True)
    paymentid = db.StringField(required=True)
    status = db.StringField(required=True)
    remainRent = db.StringField(required=True)
    date = db.StringField()


class attend(db.Document):
    date = db.StringField(required=True)
    attendance = db.ListField()

class roomChange(db.Document):
    sid = db.StringField(required=True)
    newRoom = db.StringField(required=True)
    prevRoom = db.StringField(required=True)
    email = db.StringField(required=True)