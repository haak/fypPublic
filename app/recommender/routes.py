from flask import render_template, flash, redirect, url_for, abort , request
from flask_login import login_required
# from app import movie_lens_methods
from app import omdb_test
# from app import scrape_omni
from app.debate import debate_create_explanations
from app.debate import write_to_json, write_to_json_username, debate_form, \
    update_posters, remove_movie, \
    read_from_json_username, return_ready_for_page

# USER TESTING IMPORTS:
from app.recommender.user_testing import start_user_test
from app.recommender.user_testing import next_user_testing_round
from app.recommender.user_testing import return_settings
from app.recommender.user_testing import reset_testing
from app.recommender.user_testing import check_if_trial_exists
from app.recommender.user_testing import get_user_round

from app.omdb_test import get_un_scraped_movies

# from app.debate import write_to_json
from app.recommender import app
from app.recommender.forms import RatingForm, AddMoviesForm
from app.recommender.movies import rate_movie
from app.recommender.movies import return_movies_and_ids, \
    get_current_id_for_user
from app.recommender.movies import get_omniplex_movies, \
    add_movie_to_db
# from app.recommender.explanation import get_explanation
# from app.debate import get_movies_based_on_pearson
from app.debate import delete_explanations, start_debate, update_debate
from app.debate import delete_debate
from app.debate import check_round_debate

from app.debate import rate_random_movie

# from app.recommender.explanation import create_explanation_list
# from app.recommender.explanation import read_explanation_from_db
# from app.debate import get_movie_list
# from app.recommender.explanation import Explanation
from app.recommender.explanation import create_explanation_from_db
# from app.debate import get_movie_and_poster_for_explanation
from app.debate import remove_one_movie
# from app.debate import write_movies_to_db, remove_movie_from_db
from app.debate import get_current_movies
from app.debate import get_current_movie_and_poster

from app.debate import get_movie_name_from_id

# @app.before_request
# def limit_remote_addr():
#     if request.remote_addr != '80.233.37.30':
#         abort(403)  # Forbidden


trial_round = 0
pearson = 0
title_and_poster = 0
random_explanations = 0

SCRAPE_MOVIES = 0


@app.route("/showings")
def show_movies():
    counter = 0
    user = {'id': 1, 'username': 'Alex'}
    list_of_dictionary = []
    poster_url = "/home/alex/Documents/fyp/app/static/"
    poster_urls = []
    movies = get_omniplex_movies()

    for movie in movies:
        filename = ""
        if movie["Poster"]:
            filename = movie["Poster"].split('/')[-1]
        poster_urls.append(poster_url + filename)

        imdb_id = movie["imdbID"]
        if omdb_test.has_movie_been_scraped(imdb_id) is False:
            omdb_test.scrape_omdb_with_movie_id(imdb_id)

        # this should take the actual user id not just 1
        explanation_list = omdb_test.compare_movie(imdb_id, 1)
        # this returns the common objects between a movie and the user.
        # call the functions that will give movie recommendations \
        # todo with neighbours.

        recommendations = []
        for explanation in explanation_list:
            # print(explanation)
            # change this method to instead return a dictionary that \
            # contains more than just the string to print
            # it should contain movie , user_id , rating

            output = omdb_test.print_explanation(explanation[0],
                                                 explanation[1],
                                                 explanation[2])
            recommendations.append(output)

        movie_dict = {"movie": movie, "poster": filename, "recommendation":
                      recommendations}
        list_of_dictionary.append(movie_dict)
        counter += 1
        if counter > 5:
            write_to_json(list_of_dictionary)
            write_to_json_username("alex", list_of_dictionary)
            # print(list_of_dictionary)
            # with open("text1.txt", 'w') as file1:
            #     for item in list_of_dictionary:
                    # file1.write(str(item))
            #         pass

            return render_template('recommender/showtimes.html',
                                   title='Showtimes', user=user,
                                   movies=list_of_dictionary)


@app.route('/user/<username>/rank', methods=['GET', 'POST'])
@app.route('/user/<username>/rank/', methods=['GET', 'POST'])
@login_required
def rank(username):
    form = RatingForm()
    form.movie.choices = [movie for movie in return_movies_and_ids()]
    user_id = get_current_id_for_user(username)[0]

    if check_if_trial_exists(user_id):
        round_flash = get_user_round(user_id)
        flash("Your current user trial round: " + str(round_flash))

    if form.validate_on_submit():
        if form.create_debate.data:
            delete_debate(user_id)
            delete_explanations(user_id)
            start_debate(user_id)

            settings = return_settings(user_id)
            # need to pass settings into create debate

            debate_create_explanations(username, settings)
            flash("created debate")
            if SCRAPE_MOVIES:
                get_un_scraped_movies()

        elif form.start_user_trial.data:
            check_if_trial_exists(user_id)
            start_user_test(user_id)
            settings = return_settings(user_id)
            # start user trial
            flash("you have started the user testing. Round: 1")

        elif form.next_user_trial_round.data:
            if check_if_trial_exists(user_id):

                current_round = next_user_testing_round(user_id)
                return_settings(user_id)
                # move to next round
                flash("you have moved to the next round. Round: " + str(current_round)) # noqa
            else:
                flash("you need to start the user trial")

        elif form.rate_random_movie.data:
            for i in range(0, 150):
                rate_random_movie(user_id)
            flash("rated 150 random movie")

        elif form.end_user_trial.data:
            reset_testing(user_id)
            flash("ended user trial")

        else:
            rate_movie(user_id, form.movie.data, form.rating.data)
            flash('You rated it {} out of 5'.format(form.rating.data))
    return render_template('recommender/rank.html', user=username, form=form)


@app.route('/user/<username>/debate/', methods=['GET', 'POST'])
@login_required
def debate_page(username):
    first_three_movies = []
    second_three_movies = []
    user_id = get_current_id_for_user(username)[0]
    settings = return_settings(user_id)
    # title_and_poster = settings[1]

    movies = get_current_movies(user_id)
    if len(movies) == 0:
        flash("you need to create the debate on the ranking page first")

    form = debate_form(username, movies, settings[1])

    # need to get imdb_id and poster for each movie

    # list_of_dictionary = get_movie_and_poster_for_explanation(username)
    list_of_dictionary = get_current_movie_and_poster(user_id)
    
    # need to pass the settings into the show stuff
    debate_round = check_round_debate(user_id)

    for movie in movies:
        movie_explanations = create_explanation_from_db(debate_round,
                                                        user_id, movie)

        for movie_dictionary in list_of_dictionary:
            if movie_dictionary["movie"] == movie:
                movie_dictionary["explanations"] = movie_explanations

                if settings[1] == 0:
                    print(movie_dictionary)
                    movie_dictionary["title"] = ""
                    movie_dictionary["poster"] = ""
                # this should remove the title and poster

        first_three_movies = list_of_dictionary[0:3]
        second_three_movies = list_of_dictionary[3:6]
    if form.validate_on_submit():
        
        movie_to_remove = form.movie_id.data
        update_debate(user_id, debate_round)
        if check_round_debate(user_id) == 6:
            
            remove_one_movie(user_id, movie_to_remove)
            movie = get_current_movies(user_id)
            movie_name = get_movie_name_from_id(movie[0])
            flash("you have picked movie" + " " + movie_name)
            
        else:
            remove_one_movie(user_id, movie_to_remove)

        # movie_dict_2 = remove_movie(complete_movies, movie_to_remove)
        # write_to_json_username(username, movie_dict_2)

        return redirect(url_for('recommender.debate_page', username=username))
    # flash(first_three_movies)
    # flash(second_three_movies)
    return render_template('recommender/debate.html', form=form,
                           first_three=first_three_movies,
                           second_three=second_three_movies)


@app.route('/user/<username>/add_movies', methods=['GET', 'POST'])
def add_movies(username):
    form = AddMoviesForm()
    if form.validate_on_submit():
        user_id = get_current_id_for_user(username)[0]

        # print("Ending data Value : {value}".format(value=
        # form.create_debate.data))
        add_movie_to_db(form.imdb_id.data)
        rate_movie(user_id, form.imdb_id.data, form.rating.data)
        flash("movie has been ranked and added")
    return render_template('recommender/add_movies.html', form=form)


@app.route('/walkthrough')
def walkthrough():

    return render_template('recommender/walkthough.html')

# add buttont to rate random movie
# fix title and poster.
