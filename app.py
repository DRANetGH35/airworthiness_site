from flask import Flask
from datetime import timedelta
from sqlalchemy import select
from extensions import db, login_manager, bootstrap, migrate
from models import *



def create_app():
    app = Flask(__name__)

    with open('csrfkey.txt', 'r') as file:
        app.config['SECRET_KEY'] = file.readline().strip('\n')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Time the user out after 30 minutes

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)


    #with app.app_context():



    return app