from flask import Flask, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
from forms import RegisterForm, LoginForm, AddVehicleForm, AddTaskForm
from models import db, User, Vehicle, Task
from datetime import datetime

app = Flask(__name__)
app.secret_key = "this is a secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

# with app.app_context():
#     db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -----------------------------User Routes -----------------------------------------------------------------------------

#           USER LOGIN

@app.route('/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        try:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
        except Exception:
            return redirect(url_for('login'))
        
    login_form = LoginForm()
    return render_template("index.html", form=login_form)


#           USER LOGOUT
@app.route('/user/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))


#           USER HOME
@app.route('/user/home')
@login_required
def home():
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', vehicles=vehicles)


#           USER ADD
@app.route('/user/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        clear_pass = request.form['password']
        hash_pass = generate_password_hash(clear_pass)
        user = User(email=email, name=name, password=hash_pass)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)


#           USER EDIT
@app.route('/user/edit', methods=["GET", "POST"])
@login_required
def user_edit():
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.session.query(User).get(current_user.id)
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = generate_password_hash(request.form['password'])
        db.session.commit()
        return redirect(url_for('home'))
    else:
        form.name.default = current_user.name
        form.email.default = current_user.email
        return render_template("register.html", form=form)


# ---------------------------- Vehicle Routes --------------------------------------------------------------------------

#           ADD VEHICLE
@app.route('/add_vehicle', methods=["GET", "POST"])
def add_vehicle():
    add_form = AddVehicleForm()
    if add_form.validate_on_submit():
        name = request.form['name']
        year = request.form['year']
        make = request.form['make']
        model = request.form['model']
        user_id = current_user.id
        vehicle = Vehicle(name=name, year=year, make=make, model=model, user_id=user_id)
        db.session.add(vehicle)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add_vehicle.html', form=add_form)


#           VEHICLE DETAIL
@app.route('/vehicle/<v_id>')
@login_required
def vehicle_detail(v_id):
    vehicle = Vehicle.query.get(v_id)
    tasks = vehicle.tasks
    return render_template("vehicle_detail.html", vehicle=vehicle, tasks=tasks)


#           VEHICLE DELETE
@app.route('/vehicle/delete/<v_id>')
def delete_vehicle(v_id):
    vehicle = Vehicle.query.get(v_id)
    db.session.delete(vehicle)
    db.session.commit()
    return render_template('home.html')


# -------------------------------------- Task routes -------------------------------------------------------------------

#           TASK ADD
@app.route('/task/add/<v_id>', methods=["POST", "GET"])
@login_required
def add_task(v_id):
    add_form = AddTaskForm()
    vehicle = Vehicle.query.get(v_id)
    if add_form.validate_on_submit():
        name = request.form['name']
        string_date = request.form['date']
        date = datetime.strptime(string_date, '%Y-%m-%d')
        mileage = request.form['mileage']
        task = Task(name=name, date=date, mileage=mileage, vehicle_id=v_id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('vehicle_detail', v_id=vehicle.id))

    return render_template("add_task.html", vehicle=vehicle, form=add_form)


if __name__ == "__main__":
    app.run(debug=True)
