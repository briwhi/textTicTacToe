from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(50))
    vehicles = db.relationship('Vehicle')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    name = db.Column(db.String(50))
    date = db.Column(db.Date)
    mileage = db.Column(db.Integer)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    year = db.Column(db.Integer)
    make = db.Column(db.String(40))
    model = db.Column(db.String(50))
    tasks = db.relationship("Task")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))




