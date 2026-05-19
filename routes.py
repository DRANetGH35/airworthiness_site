from flask import render_template

from extensions import db
from models import User
from app import create_app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
