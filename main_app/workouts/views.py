from flask import render_template,request,Blueprint,redirect,url_for,abort,flash
from main_app.workouts.forms import AddExerciseForm
from flask_login import current_user, login_required
from main_app.models import Exercise, Workout
from main_app import db
from flask import url_for


workouts = Blueprint('workouts',__name__)

@workouts.route('/add_workout')
@login_required
def add_workout():
    new_workout = Workout(user_id=current_user.id)
    db.session.add(new_workout)
    db.session.commit()
    return redirect(url_for('workouts.add_exercise'))

@workouts.route('/add_exercise',methods=['GET','POST'])
@login_required
def add_exercise():
    form = AddExerciseForm()
    if form.validate_on_submit():
        current_workout = Workout.query.filter_by(user_id=current_user.id)[-1]
        exercises = Exercise.query.filter_by(workout_id=current_workout.id)
        new_exercise = Exercise(workout_id=current_workout.id,
                     exercise_name=form.exercise_name.data,
                     weight=form.weight.data,
                     reps=form.reps.data)
        db.session.add(new_exercise)
        db.session.commit()
        return render_template('add_exercise.html', form=form, exercises=exercises[::-1])
    return render_template('add_exercise.html', form=form, exercises=None)

@workouts.route('/workout/int:<workout_id>')
@login_required
def workout(workout_id):
    workout = Workout.query.filter_by(id=workout_id).first()
    return render_template('workout.html',workout=workout)

@workouts.route('/delete/int:<workout_id>',methods=['POST'])
@login_required 
def delete_workout(workout_id):
    workout = Workout.query.filter_by(id=workout_id).first()
    if workout.user_id!=current_user.id:
        abort(403)
    exercises = workout.exercises
    for i in exercises:
        db.session.delete(i)
        db.session.commit()
    db.session.delete(workout)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('user.history')) 


