import sqlite3
# import jsonpickle
from app import omdb_test

from app import scrape_omni
# from app import omdb_test
from app.recommender.explanation import Explanation
db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
conn = sqlite3.connect(db_file_desktop)
c = conn.cursor()


def return_movies_and_ids():
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "select movies_2.imdb_id , movies_2.title from movies_2 ORDER BY \
        movies_2.title"
    c.execute(query)
    # print(c.fetchall())
    # this is number 1 but it needs to make a histogram as well.
    return c.fetchall()


def add_movie_rating(user_id, imdb_id, rating):
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    # print(str(user_id) + " " + imdb_id +" "+ str(rating))
    # print(type(imdb_id))
    # print("rating movie")
    query = "INSERT INTO user_ratings( user_id, imdb_id, rating)  VALUES (?, \
    ? ,?)"
    c.execute(query, (user_id, str(imdb_id), rating,))
    conn.commit()
    return


def get_current_id_for_user(username):
    db_file_desktop = "/home/alex/Documents/fyp/app.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "SELECT user.id from user where username == ?"
    c.execute(query, (username,))
    return c.fetchone()


def check_user_has_rated_movie(user_id, imdb_id):
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "select user_ratings.rating from user_ratings where user_id == ? \
        and imdb_id == ?"

    # print(type(user_id))
    # print(type(imdb_id))
    c.execute(query, (user_id, imdb_id))
    if c.fetchone() is None:
        return False
    else:
        return True
    # return c.fetchall()


def rate_movie(user_id, imdb_id, rating):
    # print("called rate movie func")
    if check_user_has_rated_movie(user_id, imdb_id):
        # print("first loop")
        update_rating(user_id, imdb_id, rating)
        return

    else:
        # print("second loop")
        add_movie_rating(user_id, imdb_id, rating)
        return


def update_rating(user_id, imdb_id, rating):
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "UPDATE user_ratings SET rating = ? where user_id == ? and \
        imdb_id == ?"
    c.execute(query, (rating, user_id, imdb_id))
    conn.commit()


def get_omniplex_movies():
    movies = scrape_omni.run()
    # print("\n\n\n\n\n\n")
    # print(movies)
    # print("\n\n\n\n\n\n")
    return movies


def get_explanation_for_movie(movies, user_id):
    # user_id = get_current_id_for_user(username)[0]
    user_id = 1
    explanation_list = []
    for movie in movies:
        imdb_id = movie["imdbID"]
        explanation_list.append(omdb_test.compare_movie(imdb_id, user_id))
    return explanation_list


def create_explanations_objects(explanations):
    explanation_objects = []
    print(explanations)
    for explanation in explanations:
        # print(explanation)
        # output = omdb_test.print_explanation(explanation[0], explanation[1],\
        #  explanation[2])
        if len(explanation) > 0:
            tmp_explanation = Explanation()
            tmp_explanation.type_id = explanation[0]
            tmp_explanation.object_id = explanation[1]
            tmp_explanation.count = explanation[2]
            tmp_explanation.get_object_string()
            explanation_objects.append(tmp_explanation)
    return explanation_objects


def get_normalized(x):
    # normalized = (x - min(x)) / (max(x) - min(x))
    return


def test_json_pickle():
    # frozen = jsonpickle.encode("test")
    # thawed = jsonpickle.decode(frozen)
    return


def add_movie_to_db(imdb_id):
    if omdb_test.has_movie_been_scraped(imdb_id) is False:
        omdb_test.scrape_omdb_with_movie_id(imdb_id)
    # print("\n\n\n\n\n")
    # print(omdb_test.has_movie_been_scraped('tt1228705'))
    # print("\n\n\n\n\n")
    return


# add_movie_rating(611, "tt0114709", 5)
# print(check_user_has_rated_movie(611, 'tt0114709'))
# update_rating(611, "tt0114709", 4)
# rate_movie(611, "tt0114709", 3)
