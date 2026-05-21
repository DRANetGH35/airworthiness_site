from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase
import os, smtplib, datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
bootstrap = Bootstrap5()

def send_verification_email(code, address):
    my_email = "dradigitalmessenger@gmail.com"
    password = os.environ.get("EMAIL_PASSWORD")
    subject = f"Verify your email address"

    message = f'Your verification code is: {code}'

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=address, msg=f"Subject:{subject}\n\n{message}")

month = datetime.datetime.now().month
day = datetime.datetime.now().day