from flask import render_template, redirect, url_for, jsonify, session
from flask import request
from flask_login import login_user, current_user
from extensions import db
from models import User
from app import create_app

app = create_app()

@app.route('/')
def index():
    print(current_user)
    print(current_user.is_authenticated)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = str(request.form.get('name'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        if User.exists(username):
            return render_template('register.html', error="Username already exists")
        new_user = User(name=username,
                        email=email,
                        password=password,
                        is_admin=False,
                        verified=False,
                        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return 'registered'
    return render_template('register.html', error="", current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == "POST":
        username = str(request.form.get('name'))
        password = str(request.form.get('password'))
        print(username, password)
        user_in_question = User.get_by_username(username)
        if user_in_question is None or user_in_question.password != password:
            return render_template('login.html', error="Incorrect username or password")
        else:
            login_user(user_in_question, remember=True)
            return redirect(url_for('index'))
    return render_template('login.html', error="", current_user=current_user)
