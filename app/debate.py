import json
import copy
import omdb
# from app import scrape_omni
import sqlite3
from app.scrape_omni import run
from app.recommender.forms import DebateForm
from app.omdb_test import has_movie_been_scraped, \
    scrape_omdb_with_movie_id, compare_movie
# from app.omdb_test import get_db
from app.movie_lens_methods import get_db
# from app.recommender.movies import get_omniplex_movies, \
# get_explanation_for_movie, create_explanations_objects
# from app.recommender.explanation import get_object_from_json
from app.recommender.movies import get_current_id_for_user
from app.recommender.explanation import get_explanation
# from app.recommender.explanation import Explanation
from app.movie_lens_methods import pearson_neighbours_by_number
# from app.scrape_omni import run_pearson
from app.scrape_omni import get_json_for_imdb, get_poster_for_movie
from ast import literal_eval
from app.recommender.explanation import Explanation
import operator
import random
from app.recommender.movies import rate_movie



def get_db():
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    return conn, c


def start_debate(user_id):
    conn, c = get_db()
    # print("start debate")
    query = "INSERT INTO debate (user_id, round) VALUES (?,1);"
    # print("\n\n\n\n\n\n\n\n\n")
    conn.execute(query, (user_id,))
    conn.commit()
    return


def update_debate(user_id, debate_round):
    conn, c = get_db()
    next_round = debate_round + 1
    query = "UPDATE debate set round = ? where user_id = ?;"
    c.execute(query, (next_round, user_id))
    conn.commit()
    return


def delete_explanations(user_id):
    conn, c = get_db()
    query = "DELETE FROM explanations where user_id == ?"
    c.execute(query, (user_id,))
    conn.commit()
    return


def delete_debate(user_id):
    conn, c = get_db()
    query = "DELETE FROM debate where user_id == ?"
    c.execute(query, (user_id,))
    conn.commit()
    return


def check_round_debate(user_id):
    conn, c = get_db()
    query = "SELECT round from debate where user_id == ?"
    c.execute(query, (user_id,))
    result = c.fetchone()
    if len(result) == 0:
        return False
    else:
        return result[0]


def write_to_json(dictionary):
    with open("./db/json/dictionary.json", "w") as outfile:
        json.dump(dictionary, outfile)


def read_from_json():
    with open('/home/alex/Documents/fyp/db/json/dictionary.json') as json_file:
        data = json.load(json_file)
    return data


def write_to_json_username_complete(username, list):
    # print("\n\n\n\n\n")
    # print("wrote to json username complete ")
    # print("\n\n\n\n\n")
    with open("./db/json/%s-complete.json" % username, "w") as outfile:
        json.dump(list, outfile)
    return


def write_to_json_username(username, list):
    # print("\n\n\n\n\n")
    # print("wrote to json username")
    # print("\n\n\n\n\n")
    with open("./db/json/%s.json" % username, "w") as outfile:
        json.dump(list, outfile)
    return


def read_from_json_username(username):
    with open("./db/json/%s.json" % username) as json_file:
        data = json.load(json_file)
    return data


def debate_form(username, movies_imdb_id, user_trial_round=1):
    counter = 1
    
    movie_list = []
    form = DebateForm()
    for movie_imdb_id in movies_imdb_id:

        if user_trial_round == 0:
            movie_list.append((movie_imdb_id, counter))
            counter += 1

        else:
            movie_name = get_movie_name_from_id(movie_imdb_id)
            movie_list.append((movie_imdb_id, movie_name))

        form.movie_id.choices = movie_list

    return form


def update_posters(movie_dict):
    # file_loc = "../../"
    for movie in movie_dict:
        movie["poster"] = movie["poster"]
    return movie_dict


def remove_movie(movie_dict, movie_id):
    movie_list = []
    for movie in movie_dict:
        if movie["movie"]["imdbID"] == movie_id:
            pass
        else:
            movie_list.append(movie)
    return movie_list


def recreate_recommendations(username):
    data = read_from_json()
    write_to_json_username(username, data)


def current_omniplex_movies():
    movies = run()
    return movies


def pearson_step_1(user_id):
    movies = run_pearson(user_id)
    return movies


###############################################################################


# def get_movie_list(user_id):
#     movie_list = []
#     if PEARSON:
#         movies = pearson_step_1(user_id)
#         for movie in movies:
#             movie_list.append(movie["imdbID"])
#     else:
#         movies = current_omniplex_movies()
#         for movie in movies:
#             movie_list.append(movie["imdbID"])
#     return movie_list


# def get_movie_and_poster_for_explanation(username):
#     # list_of_types = [1, 2, 3, 4, 8, 9, 10, 12, 13]
#     user_id = get_current_id_for_user(username)[0]
#     movies = []
#     delete_current_movies(user_id)
#     if PEARSON:
#         movies = pearson_step_1(user_id)
#     else:
#         movies = current_omniplex_movies()
#     list_of_dictionary = []
#     movies = movies[:6]
#     for movie in movies:
#         filename = ""
#         if movie["Poster"]:
#             filename = movie["Poster"].split('/')[-1]
#         imdb_id = movie["imdbID"]
#         insert_current_movie(user_id, imdb_id, filename)
#         if has_movie_been_scraped(imdb_id) is False:
#             scrape_omdb_with_movie_id(imdb_id)
#         movie_dict = {"movie": movie, "poster": filename}
#         list_of_dictionary.append(movie_dict)
#     return list_of_dictionary


def debate_create_explanations(username, settings):
    PEARSON = settings[0]
    title_and_poster = settings[1]
    random_explanations = settings[2]
    
    list_of_types = [1, 2, 3, 4, 8, 9, 10, 12, 13]
    user_id = get_current_id_for_user(username)[0]
    movies = []
    delete_current_movies(user_id)
    if PEARSON:
        movies = pearson_step_1(user_id)
    else:
        movies = current_omniplex_movies()
    # list_of_dictionary = []
    movies = movies[:6]
    for movie in movies:

        # list_of_explanations = []
        filename = ""
        if movie["Poster"]:
            filename = movie["Poster"].split('/')[-1]

        imdb_id = movie["imdbID"]
        insert_current_movie(user_id, imdb_id, filename)
        if has_movie_been_scraped(imdb_id) is False:
            scrape_omdb_with_movie_id(imdb_id)

        explanation_list = compare_movie(imdb_id, user_id)
        for explanation in explanation_list:
            if explanation[0] in list_of_types:
                expl_object = get_explanation(explanation, imdb_id, user_id, settings) # noqa
                expl_object.write_explanation_to_db()
    if PEARSON:
        ratings = get_ratings_based_on_pearson(user_id)
        # print(ratings)
        # writes  pearson results to an explanation and puts it in db
        pearson_rating_explanations(ratings, user_id)

    return


def pearson_rating_explanations(ratings, user_id):
    for movie in ratings:
        tmp_dict_string = ""
        explanation = Explanation()
        explanation.explanation_type = 16

        movie_dict = movie[0]
        tmp_dict_string += "Neighbour Ratings: \n"
        for k in movie_dict:
            tmp_dict_string += "("
            for i in range(0, k):
                tmp_dict_string += "*"
            tmp_dict_string += " : "
            tmp_dict_string += str(movie_dict[k])
            tmp_dict_string += ")"
        
        explanation.explanation = tmp_dict_string
        explanation.imdb_id = movie[1]
        explanation.count = 0
        explanation.user_id = user_id
        explanation.object_id = 0
        explanation.rating = 0.5
        explanation.write_explanation_to_db()
    return


def insert_current_movie(user_id, imdb_id, poster_filename):
    conn, c = get_db()
    query = "INSERT INTO current_movies (user_id,imdb_id,poster_filename) \
    VALUES (?,?,?)"
    c.execute(query, (user_id, imdb_id, poster_filename))
    conn.commit()
    return


def delete_current_movies(user_id):
    conn, c = get_db()
    query = "DELETE FROM current_movies where user_id == ?"
    c.execute(query, (user_id,))
    conn.commit()
    return


# returns a list of imdb_ids for the current movies for that user.
def get_current_movies(user_id):
    movie_list = []
    conn, c = get_db()

    query = "SELECT imdb_id from current_movies where user_id == ?"
    c.execute(query, (user_id,))
    result = c.fetchall()
    for movie in result:
        movie_list.append(movie[0])
    return movie_list


def remove_one_movie(user_id, imdb_id):

    conn, c = get_db()
    query = "DELETE FROM current_movies where user_id == ? and imdb_id == ?"
    c.execute(query, (user_id, imdb_id))
    conn.commit()
    return


def json_for_explanations(explanation_objects):
    json_list = []
    for explanation in explanation_objects:
        json_frozen = explanation.get_json_for_object()
        json_list.append(json_frozen)
    return json_list


def return_ready_for_page(movie_dict):
    complete_movies = []
    incomplete_movies = []
    for movie in movie_dict:
        # print("\n\n\n\n\n\n")
        # print(movie)
        # print("\n\n\n\n\n\n")
        movie4 = copy.deepcopy(movie)
        movie2 = remove_first_explanation(movie)
        complete_movies.append(movie2)
        movie3 = remove_all_but_first_explanation(movie4)

        incomplete_movies.append(movie3)
    return(complete_movies, incomplete_movies)


def remove_all_but_first_explanation(first_movie):
    explanations = first_movie["explanations"]
    for explanation in explanations:
        if "expr_rating" in explanation and "explanation" in explanation:
            pass
        else:
            del explanations[explanations.index(explanation)]

    newlist = sorted(explanations, key=lambda k: k["expr_rating"])
    first_movie["explanations"] = newlist[-1]
    return first_movie


def remove_first_explanation(not_firstmovie):
    explanations = not_firstmovie["explanations"]
    for explanation in explanations:
        if "expr_rating" in explanation and "explanation" in explanation:
            pass
        else:
            del explanations[explanations.index(explanation)]
    # print(explanations)
    newlist = sorted(explanations, key=lambda k: k["expr_rating"])
    del newlist[-1]
    not_firstmovie["explanations"] = newlist
    return not_firstmovie


# get top 6 movies to recommend to a user_id
def get_movies_based_on_pearson(user_id):
    total = {}
    similarity_sum = {}

    top_neighbours = pearson_neighbours_by_number(user_id)
    for neighbour in top_neighbours:
        neighbour_id = neighbour[0]
        neighbour_pearson = neighbour[1]
        neighbour_ratings = get_rating_and_id_for_user(neighbour_id)

        for rating in neighbour_ratings:
            # check if imdb_id in list
            imdb_id = rating[0]
            score = rating[1]
            if score > 0:
                if imdb_id not in total:
                    total[imdb_id] = 0
                    similarity_sum[imdb_id] = 0
                total[imdb_id] += score * neighbour_pearson
                similarity_sum[imdb_id] += neighbour_pearson
    ranking = [(tot/similarity_sum[movieid], movieid) for movieid, tot in total.items()] # noqa
    # ranking.sort()
    # ranking.reverse()
    ranking.sort(key=operator.itemgetter(0), reverse=True)

    # ranked_total = [(tot, movieid) for movieid, tot in total.items()]  # noqa
    # ranked_total.sort(key=operator.itemgetter(0), reverse=True)
    # print(ranked_total)
    return ranking[:6]


def get_ratings_based_on_pearson(user_id):

    movies = get_current_movies(user_id)
    list_of_movies = []
    
    top_neighbours = pearson_neighbours_by_number(user_id)

    for movie in movies:
        ratings = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for neighbour in top_neighbours:
            # print("neighbour" + str(neighbour))
            # print("movie" + str(movie))
            neighbour_id = neighbour[0]
            neighbour_ratings = get_rating_for_user(neighbour_id, movie)
            if neighbour_ratings is not None:
                # print(neighbour_ratings)
                rating = neighbour_ratings

                if neighbour_ratings in ratings:
                    ratings[rating] += 1
        list_of_movies.append((ratings, movie))
    return list_of_movies


def get_rating_and_id_for_user(user_id):
    conn, c = get_db()
    query = "select imdb_id,rating from user_ratings where user_id == ?"
    c.execute(query, (user_id,))
    response = c.fetchall()
    return response


def get_rating_for_user(user_id, imdb_id):
    conn, c = get_db()
    query = "select rating from user_ratings where user_id == ? and imdb_id == ?"
    c.execute(query, (user_id, str(imdb_id)))
    response = c.fetchone()
    if response is None:
        return False
    else:
        return response[0]


def get_movie_name_from_id(imdb_id):
    conn, c = get_db()
    query = "SELECT title from movies_2 where imdb_id == ?"
    c.execute(query, (imdb_id,))
    result = c.fetchone()
    return result[0]


def run_pearson(user_id):
    movies_jsons = []
    omdb.set_default('apikey', "")
    # movies = get_omniplex_movies()
    # print("userid")
    # print(user_id)
    movies = get_movies_based_on_pearson(user_id)
    # print("movies that are in run_pearson")
    for movie in movies:
        movie_json = get_json_for_imdb(movie[1])
        if movie_json is not False:
            movie_dict = literal_eval(movie_json)
            get_poster_for_movie(movie_dict)
            movies_jsons.append(movie_dict)
    return movies_jsons


def get_current_movie_and_poster(user_id):
    movie_list = []
    conn, c = get_db()

    query = "SELECT imdb_id, poster_filename from current_movies where user_id == ?"
    c.execute(query, (user_id,))
    result = c.fetchall()
    for movie in result:
        movie_title = get_movie_name_from_id(movie[0])
        movie_dict = {"movie": movie[0], "title": movie_title, "poster": movie[1]}
        movie_list.append(movie_dict)
    return movie_list


def rate_random_movie(user_id):
    list_of_movies = get_list_of_movies()
    rand_movie_idx = random.randint(1, len(list_of_movies)-1)
    movie = list_of_movies[rand_movie_idx]

    rand_score = random.randint(0, 5)

    rate_movie(user_id, movie, rand_score)
    #get all movies in db
    # pick random number 
    # rate that movie a random number between 0 and 6


def get_list_of_movies():
    conn, c = get_db()    
    query = "SELECT imdb_id from movies_2 "
    c.execute(query)
    result = c.fetchall()
    conn.commit()
    movies = clean_list_of_movies(result)

    return movies


def clean_list_of_movies(movie_list):
    clean_list = []
    for movie in movie_list:
        clean_list.append(movie[0])
    return clean_list
