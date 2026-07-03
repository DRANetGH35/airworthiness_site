from flask import render_template, redirect, url_for, jsonify, session
from flask import request
from flask_login import login_user, current_user, logout_user, login_required
from extensions import db, send_verification_email
from models import User, Plane, TimeEntry, MaintenanceEntry, Engine, Overhaul
from app import create_app
from werkzeug.security import generate_password_hash, check_password_hash
import random
from sqlalchemy import select, delete
import datetime
from decorators import admin_required

app = create_app()

def update_Totals(user, plane):
    user.updateHobbsTime()
    plane.updateTachHours()
    engine = plane.get_latest_engine()
    engine.updateTachHours()
    overhaul = engine.get_latest_overhaul()
    overhaul.updateTachHours()

def getRecentEntries(plane):
    engine = plane.get_latest_engine()
    overhaul = engine.get_latest_overhaul()
    result = db.session.execute(select(TimeEntry).where(TimeEntry.overhaul_id == overhaul.id)).scalars().all()[-5::1]
    return result

@app.route('/')
def index():
    planes = []
    if current_user.is_authenticated:
        planes = db.session.execute(select(Plane).where(Plane.user_id == current_user.id)).scalars().all()
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
                        verification_code=verification_code,
                        hobbs_time=0
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

@app.route('/admin')
@admin_required
def admin_panel():
    users = db.session.execute(select(User)).scalars().all()
    for user in users:
        user.total_entries = 0
        for plane in user.planes:
            user.total_entries += len(plane.timetable)
    return render_template('admin/admin_panel.html', users=users)

@app.route('/plane_data/<plane_id>')
def plane_data(plane_id):
    plane = db.session.execute(select(Plane).where(Plane.id == plane_id)).scalar()
    update_Totals(current_user, plane)
    maintenance_table = db.session.execute(select(MaintenanceEntry).where(MaintenanceEntry.plane_id == plane_id)).scalars().all()
    time_table = getRecentEntries(plane)
    engine = plane.get_latest_engine()
    return render_template('plane_data_page.html', plane=plane, time_table=time_table, maintenance_table=maintenance_table, engine=engine)

@login_required
@app.route('/time_table/plane_<plane_id>')
def time_table(plane_id):
    plane = db.session.execute(select(Plane).where(Plane.id == plane_id)).scalar()
    update_Totals(current_user, plane)
    engine_table = db.session.execute(select(Engine).where(Engine.plane_id == plane_id)).scalars().all()
    time_table = db.session.execute(select(TimeEntry).where(TimeEntry.plane_id == plane.id)).scalars().all()
    return render_template('time_table.html', time_table=time_table, plane=plane, engine_table=engine_table, current_user=current_user)

@login_required
@app.route('/engine_<engine_id>')
def view_engine(engine_id):
    engine = db.session.execute(select(Engine).where(Engine.id == engine_id)).scalar()
    plane = engine.plane
    update_Totals(current_user, plane)
    return render_template('view_engine.html', engine=engine, current_user=current_user)

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
                          user_id=current_user.id,
                          initial_tach_hours=request.form.get('aircraft-hours'),
                          tach_hours=request.form.get('aircraft-hours'))
        db.session.add(new_plane)
        new_engine = Engine(plane=new_plane,
                            initial_tach_hours = request.form.get('engine-hours'),
                            tach_hours = request.form.get('engine-hours'),
                            plane_id=new_plane.id,
                            created=datetime.datetime.now())
        db.session.add(new_engine)
        new_overhaul = Overhaul(engine=new_engine,
                                engine_id=new_engine.id,
                                created=datetime.datetime.now(),
                                initial_tach_hours=request.form.get('overhaul-hours'),
                                tach_hours=request.form.get('overhaul-hours'))
        db.session.add(new_overhaul)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_plane.html')

@app.route('/plane_data/<engine_id>/overhaul')
def overhaul(engine_id):
    engine = db.session.execute(select(Engine).where(Engine.id == engine_id)).scalar()
    new_overhaul = Overhaul(engine=engine,
                            engine_id=engine.id,
                            created=datetime.datetime.now(),
                            tach_hours=0)
    db.session.add(new_overhaul)
    db.session.commit()
    return redirect(request.referrer)

@app.route('/plane_data/<plane_id>/add_new_engine', methods=['GET', 'POST'])
def new_engine(plane_id):
    if request.method == "POST":
        plane = db.session.execute(select(Plane).where(Plane.id == plane_id)).scalar()
        new_engine = Engine(plane=plane,
                            initial_tach_hours=request.form.get('engine-hours'),
                            tach_hours=0,
                            plane_id=plane.id,
                            created=datetime.datetime.now())
        db.session.add(new_engine)
        new_overhaul = Overhaul(engine=new_engine,
                                engine_id=new_engine.id,
                                created=datetime.datetime.now(),
                                tach_hours=0,
                                initial_tach_hours=request.form.get('overhaul-hours'))
        db.session.add(new_overhaul)
        db.session.commit()
        return redirect(f'/plane_data/{plane_id}')
    return render_template('add_new_engine.html', plane_id=plane_id)

@login_required
@app.route('/add_time_entry', methods=['POST'])
def add_time_entry():
    tach_time_input = float(request.form.get('tach_time'))
    plane_id = request.referrer.split('/')[-1]
    plane = db.session.execute(select(Plane).where(Plane.id == plane_id)).scalar()
    latest_engine = plane.get_latest_engine()
    latest_overhaul = latest_engine.get_latest_overhaul()
    new_time_entry = TimeEntry(
        created = datetime.datetime.now(),
        tach_time = tach_time_input,
        plane=plane,
        plane_id=plane_id,
        engine=latest_engine,
        engine_id=latest_engine.id,
        overhaul=latest_overhaul,
        overhaul_id=latest_overhaul.id
    )
    db.session.add(new_time_entry)
    db.session.commit()
    return redirect(f'/plane_data/{plane_id}')

@login_required
@app.route('/deleteTimeEntry/<id>')
def deleteTimeEntry(id):
    db.session.execute(delete(TimeEntry).where(TimeEntry.id == id))
    db.session.commit()
    return redirect(request.referrer)

@login_required
@app.route('/edit_time_entry/<id>', methods=['POST'])
def editTimeEntry(id):
    entry = db.session.execute(select(TimeEntry).where(TimeEntry.id == id)).scalar()
    entry.tach_time = request.form.get('value')
    db.session.commit()
    return redirect(request.referrer)


@login_required
@app.route('/plane_data/<plane_id>/maintenance_item/<maintenance_item_id>', methods=['GET', 'POST'])
def add_maintenance_entry(plane_id, maintenance_item_id):
    plane = db.session.execute(select(Plane).where(Plane.id == plane_id)).scalar()
    maintenance_item = "new" if maintenance_item_id == "new" else db.session.execute(select(MaintenanceEntry).where(MaintenanceEntry.id == maintenance_item_id)).scalar()
    if request.method == "POST":
        tach_last_completed = None
        date_last_completed = None
        interval_hours = None
        interval_months = None
        due_tach = None
        date_due = None

        plane_id = plane_id
        plane = db.session.execute(select(Plane).where(Plane.id == plane_id)).scalar()
        description = request.form.get('description')
        maintenance_type = request.form.get('maintenance_type')
        interval = request.form.get('interval_option') == "interval"
        if interval:
            if request.form.get('tach_hours_last_complete') != '':
                tach_last_completed = float(request.form.get('tach_hours_last_complete'))
            if request.form.get('date_last_complete') != '':
                date_last_completed = datetime.datetime.strptime(request.form.get('date_last_complete'), '%Y-%m-%d')
            if request.form.get('interval_hours') is not None:
                interval_hours = float(request.form.get('interval_hours'))
            if request.form.get('interval_months') != None:
                interval_months = float(request.form.get('interval_months'))
            due_tach = tach_last_completed + interval_hours if interval_hours is not None else None
            date_due = date_last_completed + datetime.timedelta(days=interval_months * 30) if interval_months is not None else None
        else:
            due_tach = request.form.get('tach_hours_due') if request.form.get('tach_hours_due') != '' else None
            if request.form.get('date_due') != '':
                date_due = datetime.datetime.strptime(request.form.get('date_due'), '%Y-%m-%d')
        if maintenance_item_id == "new":
            new_maintenance_item = MaintenanceEntry(description=description,
                                                    maintenance_type=maintenance_type,
                                                    interval=interval,
                                                    tach_last_completed=tach_last_completed,
                                                    date_last_completed=date_last_completed,
                                                    interval_hours=interval_hours,
                                                    interval_months=interval_months,
                                                    due_date=date_due,
                                                    due_tach=due_tach,
                                                    status='incomplete',
                                                    plane=plane,
                                                    plane_id=plane.id)

            db.session.add(new_maintenance_item)
        else:
            maintenance_item = db.session.execute(select(MaintenanceEntry).where(MaintenanceEntry.id == maintenance_item_id)).scalar()
            maintenance_item.maintenance_type=maintenance_type
            maintenance_item.interval=interval
            maintenance_item.tach_last_completed=tach_last_completed
            maintenance_item.date_last_completed=date_last_completed
            maintenance_item.interval_hours=interval_hours
            maintenance_item.interval_months=interval_months
            maintenance_item.due_date=date_due
            maintenance_item.due_tach=due_tach
            maintenance_item.plane=plane
            maintenance_item.plane_id=plane.id
        db.session.commit()
        return redirect(f'/plane_data/{plane_id}')
    return render_template('add_maintenance_item.html', plane=plane, maintenance_item_id=maintenance_item_id, maintenance_item=maintenance_item)

@login_required
@app.route('/verify', methods=['POST'])
def verify():
    verification_code = str(request.form.get('verification_code'))
    if request.form.get("verification_code") == current_user.verification_code:
        current_user.set_verified(True)
        error = "incorrect code"
        return render_template('index.html', current_user=current_user, error=error)
    return redirect(url_for('index'))

@app.route('/fetch_maintenance_item/<id>')
def fetchMaintenanceItem(id):
    maintenance_item = db.session.execute(select(MaintenanceEntry).where(MaintenanceEntry.id == id)).scalar()
    return jsonify({"status": maintenance_item.status,
                    "description": maintenance_item.description,
                    "maintenance_type": maintenance_item.maintenance_type,
                    "interval": maintenance_item.interval,
                    "due_date": maintenance_item.due_date.strftime('%Y-%m-%d') if maintenance_item.due_date is not None else None,
                    "due_tach": maintenance_item.due_tach,
                    "tach_last_completed": maintenance_item.tach_last_completed,
                    "date_last_completed": maintenance_item.date_last_completed.strftime('%Y-%m-%d') if maintenance_item.date_last_completed is not None else None,
                    "interval_hours": maintenance_item.interval_hours,
                    "interval_months": maintenance_item.interval_months})

@app.route('/change_maintenance_status', methods=['GET', 'POST'])
def changeMaintenanceStatus():
    id = request.form.get('id')
    selected_value = request.form.get('selected_value')
    if selected_value == "delete":
        db.session.execute(delete(MaintenanceEntry).where(MaintenanceEntry.id == id))
        db.session.commit()
    else:
        maintenance_item = db.session.execute(select(MaintenanceEntry).where(MaintenanceEntry.id == id)).scalar()
        maintenance_item.status = selected_value
        db.session.commit()
    return redirect(request.referrer)

@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html')

@app.route('/test')
def test():
    print('test')
    return redirect(request.referrer)