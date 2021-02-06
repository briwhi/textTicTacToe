from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, validators
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets.html5 import DateInput


class RegisterForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField(label='Submit')


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Log In')


class AddVehicleForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    year = IntegerField(label="Year")
    make = StringField(label="Make")
    model = StringField(label="Model", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class AddTaskForm(FlaskForm):
    name = StringField(label="Description", validators=[DataRequired()])
    date = DateField(label="Date", widget=DateInput(), validators=[DataRequired()])
    mileage = IntegerField(label="Mileage")
    submit = SubmitField(label="Submit")