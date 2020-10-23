from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField 
from wtforms.validators import DataRequired

class AddUserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()]) 

class NewGameForm(FlaskForm):
    player_one = SelectField("Player 1", choices=[])
    player_two = SelectField("Player 2", choices=[])
    starting_player = SelectField("Starting Player", choices=[]) 

class ScoreForm(FlaskForm):
    user_id  = StringField("user_id")
    score  = IntegerField("Score", default=1, validators=[DataRequired(),])

class ScoreForm2(FlaskForm):
    user_id2  = StringField("user_id")
    score2  = IntegerField("Score", default=1, validators=[DataRequired(),])