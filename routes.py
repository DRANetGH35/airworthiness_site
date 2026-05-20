from flask import render_template
from flask import request
from extensions import db
from models import User
from app import create_app

app = create_app()

@app.route('/')
def index():
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
                        is_active=False
                        )
        db.session.add(new_user)
        db.session.commit()
        return 'registered'
    return render_template('register.html', error="")
