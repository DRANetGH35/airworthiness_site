from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase
import os, smtplib, datetime
from flask_migrate import Migrate

class Base(DeclarativeBase):
    pass

from sqlalchemy import MetaData
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
Base.metadata.naming_convention = naming_convention

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
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