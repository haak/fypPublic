from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField


class RatingForm(FlaskForm):
    movie = SelectField("Movie")
    rating = SelectField("Rating", choices=[("5", 5), ("4", 4), ("3", 3),
                                            ("2", 2), ("1", 1)])
    submit = SubmitField('Rate Movie')
    create_debate = SubmitField(label='create debate')
    start_user_trial = SubmitField(label='create user trial')
    next_user_trial_round = SubmitField(label='move to next user trial round')
    end_user_trial = SubmitField(label='end user trial')
    rate_random_movie = SubmitField(label='rate 150 random movies')



class DebateForm(FlaskForm):
    movie_id = SelectField("Movie", choices=[])
    submit = SubmitField('Remove Movie')


class AddMoviesForm(FlaskForm):
    imdb_id = StringField('IMDB ID')
    title = StringField("Title")
    year = StringField("Year")
    rating = SelectField("Rating", choices=[("5", 5), ("4", 4), ("3", 3),
                                            ("2", 2), ("1", 1)])
    submit = SubmitField('Add and rate movie')
