from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class AddExerciseForm(FlaskForm):
    exercise_name = StringField('Name', validators=[DataRequired()])
    weight = IntegerField('Weight',validators=[DataRequired()])
    reps = IntegerField('Reps', validators=[DataRequired()])
    submit = SubmitField('Add Exercise')