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
    app.config['SERVER_NAME'] = 'airworthiness.dradigital.net'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True

    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)


    #with app.app_context():



    return app