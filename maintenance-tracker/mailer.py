import smtplib
from models import User, db, Vehicle, Task
from config import *


class Mailer():
    def __init__(self, user):
        self.user = user
        self.db = db
        self.email = "APP_EMAIL"
        self.password = "APP_EMAIL_PASSWORD"

    def send_mail(self):
        msg = self.get_message()
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=APP_EMAIL, password=APP_EMAIL_PASSWORD)
            connection.sendmail(from_addr=APP_EMAIL,
                                to_addrs=self.user.email,
                                msg=msg
                                )

    def get_message(self):
        message = ""
        vehicles = Vehicle.query.filter_by(user_id=self.user.id).all()
        for vehicle in vehicles:
            message += f"{vehicle.name} {vehicle.year} {vehicle.make} {vehicle.model} \n"
            for task in vehicle.tasks:
                message += f"   {task.name} {task.date} {task.mileage}\n"
        return message


