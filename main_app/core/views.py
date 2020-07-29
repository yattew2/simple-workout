from flask import render_template,request,Blueprint
from main_app.models import Workout
from flask_login import current_user

core = Blueprint('core',__name__)

@core.route('/')
def index():
    welcome_text = 'SignUp or Login to begin tracking your workouts'
    if current_user.is_authenticated:
        welcome_text = 'Click on "new Workout" to begin working out'
    return render_template('index.html',welcome_text=welcome_text)