from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets.html5 import DateInput
from models import User


class RegisterForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(),Length(min=8)])
    submit = SubmitField(label='Register')


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Log In')


class AddVehicleForm(FlaskForm):
    name = StringField(label='Name')
    year = IntegerField(label="Year")
    make = StringField(label="Make")
    model = StringField(label="Model", validators=[DataRequired()])
    submit = SubmitField(label="Add")


class AddTaskForm(FlaskForm):
    name = StringField(label="Description")
    date = DateField(label="Date", widget=DateInput())
    mileage = IntegerField(label="Mileage")
    submit = SubmitField(label="Submit")