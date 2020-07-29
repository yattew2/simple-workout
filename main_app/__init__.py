from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://iglsnmmcnywmra:b98450899319186d26a5469588290e879c9ea9c452867ba1decd0aa19b3edd09@ec2-50-19-26-235.compute-1.amazonaws.com:5432/d26c0trro17b5q'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"

from main_app.core.views import core
from main_app.user.views import user
from main_app.workouts.views import workouts
app.register_blueprint(core)
app.register_blueprint(user)
app.register_blueprint(workouts)