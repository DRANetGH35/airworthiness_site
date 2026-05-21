from flask import render_template, redirect, url_for, jsonify, session
from flask import request
from flask_login import login_user, current_user, logout_user, login_required
from extensions import db, send_verification_email
from models import User, Plane, TimeEntry
from app import create_app
from werkzeug.security import generate_password_hash, check_password_hash
import random
from sqlalchemy import select
import datetime

app = create_app()

@app.route('/')
def index():
    planes = db.session.execute(select(Plane)).scalars().all()
    return render_template('index.html', current_user=current_user, planes=planes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = str(request.form.get('name'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        verification_code = f"{random.randint(0, 99999):05}"
        if User.exists(username):
            return render_template('register.html', error="Username already exists")
        new_user = User(name=username,
                        email=email,
                        password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8),
                        is_admin=False,
                        verified=False,
                        verification_code=verification_code
                        )
        db.session.add(new_user)
        db.session.commit()
        send_verification_email(verification_code, email)
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html', error="", current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == "POST":
        username = str(request.form.get('name'))
        password = str(request.form.get('password'))
        user_in_question = User.get_by_username(username)
        if user_in_question is None or not check_password_hash(user_in_question.password, password):
            return render_template('login.html', error="Incorrect username or password")
        else:
            login_user(user_in_question, remember=True)
            return redirect(url_for('index'))
    return render_template('login.html', error="", current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/plane_data/<plane_id>')
def plane_data(plane_id):
    plane = db.session.execute(select(Plane).where(Plane.id == plane_id)).scalar()
    time_table = db.session.execute(select(TimeEntry).where(TimeEntry.plane_id == plane_id)).scalars().all()
    print(time_table)
    return render_template('plane_data_page.html', plane=plane, time_table=time_table)

@login_required
@app.route('/add_plane', methods=['GET', 'POST'])
def add_plane():
    if request.method == "POST":
        plane_name = request.form.get('plane')
        if plane_name == "":
            error = "Plane name must not be empty"
            return render_template('add_plane.html', error=error)
        new_plane = Plane(name=plane_name,
                          user=current_user,
                          user_id=current_user.id)
        db.session.add(new_plane)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_plane.html')

@login_required
@app.route('/add_time_entry', methods=['POST'])
def add_time_entry():
    plane_id = request.referrer.split('/')[-1]
    plane = db.session.execute(select(Plane).where(Plane.id == plane_id)).scalar()
    new_time_entry = TimeEntry(
        created = datetime.datetime.now(),
        tach_time = request.form.get('tach_time'),
        plane=plane,
        plane_id=plane_id
    )
    db.session.add(new_time_entry)
    db.session.commit()
    return redirect(f'/plane_data/{plane_id}')

@login_required
@app.route('/verify', methods=['POST'])
def verify():
    verification_code = str(request.form.get('verification_code'))
    if request.form.get("verification_code") == current_user.verification_code:
        current_user.set_verified(True)
        error = "incorrect code"
        return render_template('index.html', current_user=current_user, error=error)
    return redirect(url_for('index'))