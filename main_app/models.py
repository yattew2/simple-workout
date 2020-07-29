from main_app import db
from flask_login import UserMixin
from main_app import login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    workouts = db.relationship('Workout',backref='user')

    def __init__(self,username,password):
        self.username = username
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exercises = db.relationship('Exercise',backref='workout')
    time = db.Column(db.DateTime,nullable=False,default=datetime.now)
    def __init__(self,user_id):
        self.user_id = user_id

class Exercise(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    exercise_name = db.Column(db.String, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    def __init__(self,workout_id,exercise_name,weight,reps):
        self.workout_id = workout_id
        self.exercise_name = exercise_name
        self.weight = weight
        self.reps = reps

    
    

