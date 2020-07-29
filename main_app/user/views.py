from flask import render_template,request,Blueprint,redirect,url_for,abort
from main_app.user.forms import LoginForm, RegistrationForm
from main_app.models import User, Workout, Exercise
from main_app import db
from flask_login import login_required, current_user, login_user, logout_user



user = Blueprint('user',__name__)

@user.route('/signup',methods=['GET','POST'])
def signup():
    if current_user.is_anonymous:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data,password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('core.index'))
        return render_template('signup.html',form=form)
    else:
        abort(404)

@user.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_anonymous:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.check_password(form.password.data):
                    login_user(user)
                    # next = request.args.get('next')
                    # if not (next):
                    #     return flask.abort(400)
                    return redirect(url_for('core.index'))
        return render_template('login.html',form=form,errors=form.errors.items())
    else:
        abort(404)

@user.route('/history')
@login_required
def history():
    page = request.args.get('page',1,type=int)
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.time.desc()).paginate(page=page,per_page=5)
    work_exc = {}
    for i in workouts.items:
        ex_str = ''
        ex_list = []
        for j in i.exercises:
            if j.exercise_name not in ex_list:
                ex_str += str(j.exercise_name + ", ")
                ex_list.append(j.exercise_name)
        work_exc[i] = ex_str.rstrip().rstrip(',')
    return render_template('history.html',work_exc=work_exc,workouts=workouts)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))
    
