from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from forms import RegisterForm, LoginForm, AddVehicleForm, AddTaskForm
from models import db, User, Vehicle, Task
from mailer import Mailer

app = Flask(__name__)
app.secret_key = "this is a secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        try:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
        except Exception:
            return redirect(url_for('login'))
        
    return render_template("index.html", form=form)


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
    user = User()
    form = RegisterForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        clear_pass = request.form['password']
        hash_pass = generate_password_hash(clear_pass)
        user.password = hash_pass
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)


#           USER EDIT
@app.route('/user/edit', methods=["GET", "POST"])
@login_required
def user_edit():
    user = current_user
    form = RegisterForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template("register.html", form=form)


# USER DELETE
@app.route('/user/delete')
@login_required
def user_delete():
    db.session.delete(current_user)
    db.session.commit()
    return redirect(url_for('login'))


# USER SEND MAIL
@app.route('/user/send_mail')
@login_required
def send_mail():
    mailer = Mailer(current_user)
    mailer.send_mail()
    flash("Email was sent")
    return redirect(url_for('home'))


# ---------------------------- Vehicle Routes --------------------------------------------------------------------------
#           ADD VEHICLE
@app.route('/add_vehicle', methods=["GET", "POST"])
def add_vehicle():
    vehicle = Vehicle()
    form = AddVehicleForm(obj=vehicle)
    if form.validate_on_submit():
        form.populate_obj(vehicle)
        vehicle.user_id = current_user.id
        db.session.add(vehicle)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('add_vehicle.html', form=form)


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
    return redirect(url_for('home'))


#           VEHICLE EDIT
@app.route('/vehicle/edit/<v_id>', methods=["GET", "POST"])
def edit_vehicle(v_id):
    vehicle = Vehicle.query.get(v_id)
    form = AddVehicleForm(obj=vehicle)
    if form.validate_on_submit():
        form.populate_obj(vehicle)
        db.session.commit()
        return redirect(url_for('vehicle_detail', v_id=vehicle.id))
    else:
        return render_template("add_vehicle.html", form=form)


# -------------------------------------- Task routes -------------------------------------------------------------------

#           TASK ADD
@app.route('/task/add/<v_id>', methods=["POST", "GET"])
@login_required
def add_task(v_id):
    vehicle = Vehicle.query.get(v_id)
    task = Task()
    form = AddTaskForm(obj=task)
    if form.validate_on_submit():
        form.populate_obj(task)
        task.vehicle_id = v_id
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('vehicle_detail', v_id=vehicle.id))
    else:
        return render_template("add_task.html", vehicle=vehicle, form=form)


# TASK EDIT
@app.route('/task/edit/<v_id>/<t_id>', methods=['GET', 'POST'])
def edit_task(v_id, t_id):
    task = Task.query.get(t_id)
    form = AddTaskForm(obj=task)
    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        return redirect(url_for('vehicle_detail', v_id=v_id))
    else:
        return render_template("add_task.html", form=form)


# TASK DELETE
@app.route('/task/delete/<v_id>/<t_id>')
def delete_task(v_id, t_id):
    task = Task.query.get(t_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('vehicle_detail', v_id=v_id))


if __name__ == "__main__":
    app.run(debug=True)
