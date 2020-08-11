import sqlite3
from scipy.stats import pearsonr
import math
# calculate the Pearson's correlation between two variables
# from numpy.random import randn
# from numpy.random import seed
# from operator import itemgetter
from app import neighborhood_testing
db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
conn = sqlite3.connect(db_file_desktop)
c = conn.cursor()


def get_db():
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    return conn, c


# Method 1
def find_ratings_for_movie(imdb_id):
    # this can be called and then make a histogram
    # this needs to make a histogram
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "select rating, COUNT(rating) from user_ratings where imdb_id = ? \
        GROUP BY rating"
    c.execute(query, (imdb_id,))
    # print(c.fetchall())
    # this is number 1 but it needs to make a histogram as well.
    return c.fetchall()


# MovieLens Method 2
def past_performance(movie_id):
    # maybe this should also do it based on actors.
    # ive no idea what this is.
    # could be how far each person review is from the avg
    # or how far youres is from the avg
    # is this avg review for a director.
    query_for_director = """SELECT SUM(rating)/COUNT(rating) FROM movies_2 WHERE imdb_id in (
                            SELECT movie_id from movie_to_objects WHERE \
                                object_id == (SELECT object_id from
                            movie_to_objects WHERE movie_id == ? AND type == \
                                3) AND type == 3);
                            """
    c.execute(query_for_director, (movie_id,))
    response = c.fetchone()
    if response is not None:
        return response[0]
    else:
        return None


# 6 favourite actor or actress.
def favourite_actor_or_actress(user_id):
    # this returns #top favourite actors
    top = 3
    actor_dictionary = {}
    query_for_actors = """SELECT  t1.type,t1.object_id , COUNT(*)FROM (
                        (SELECT movie_id,type,object_id FROM movie_to_objects \
                            WHERE type == 1) t1
                        LEFT JOIN
                        (SELECT movie_id, type, object_id FROM \
                            movie_to_objects  GROUP BY object_id, type , \
                                movie_id
                        HAVING movie_id in (SELECT imdb_id FROM \
                            movie_id_to_imdb_id WHERE movie_id in
                        (SELECT movie_id FROM user_to_movie WHERE user_id \
                            == ?))
                        ) t2 on t1.object_id = t2.object_id AND t1.type = \
                            t2.type)
                        GROUP BY t1.type,t1.object_id ORDER BY t1.type;"""
    c.execute(query_for_actors, (user_id, ))
    for actor in c.fetchall():
        actor_dictionary[actor[1]] = actor[2]
    top_actors = sorted(actor_dictionary, key=actor_dictionary.get,
                        reverse=True)[:top]
    # print(top_actors)
    return


# 8
def won_awards(movie_id):
    query_for_awards = """SELECT awards.awards  FROM awards WHERE object_id in (
    SELECT movie_to_objects.object_id from movie_to_objects WHERE object_id \
        == (SELECT object_id from
                        movie_to_objects WHERE movie_id == ? AND type == 11) \
                            AND type == 11);
    """
    c.execute(query_for_awards, (movie_id,))
    response = c.fetchone()
    if response is not None:
        return response[0]
    else:
        return None


# 15
def overall_percent_rated(movie_id):
    threshold = 4

    query_for_threshold_ratings = "SELECT COUNT(user_ratings.rating) from \
        user_ratings WHERE imdb_id == ? " \
                              "and  user_ratings.rating >= ?"

    query_for_total_ratings = " SELECT COUNT(user_ratings.rating) FROM \
        user_ratings WHERE imdb_id == ? "

    c.execute(query_for_total_ratings, (movie_id,))
    total_ratings = c.fetchone()
    if total_ratings is not None:
        c.execute(query_for_threshold_ratings, (movie_id, threshold))
        threshold_ratings = c.fetchone()
        if threshold_ratings is not None:
            return threshold_ratings[0]/total_ratings[0] * 100
        else:
            return None
    else:
        return None


# 21
def overall_avg_rating(movie_id):
    query = "SELECT rating from movies_2 where movies_2.imdb_id == ?"
    c.execute(query, (movie_id, ))
    response = c.fetchone()
    if response is not None:
        return response[0]
    else:
        return None


def find_neighbours_sql(user_id):
    conn, c = get_db()

    user_list = []
    query = "SELECT DISTINCT user_ratings.user_id from user_ratings where \
        imdb_id in (SELECT " \
            "user_ratings.imdb_id from user_ratings where user_id == ?) and \
                user_id != ? "
    c.execute(query, (user_id, user_id))
    response = c.fetchall()
    for user in response:
        user_list.append(user[0])
    if response is not None:
        return user_list
    else:
        return None


# 10
def return_number_of_neighbours(user_id):
    neighbours = find_neighbours_sql(user_id)
    return len(neighbours)


def find_neighbour_ratings(movie_id, neighbours):
    ratings = []
    for neighbour in neighbours:
        query = "SELECT user_ratings.rating from user_ratings where user_id == \
            ? and movie_id == ?"
        c.execute(query, (neighbour, movie_id))
        tmp_rating = c.fetchone()
        if tmp_rating is not None:
            ratings.append(tmp_rating[0])
    return ratings


def rating_of_closest_neighbour(movie_id, user_id):
    # percent difference is difference between ratings / mean of those ratings
    neighbours = neighborhood_testing.find_n_neighbours(user_id)
    closest_neighbour = neighbours[0]
    # print(user_id, closest_neighbour)
    total_agreement = 0

    query = "SELECT a.rating , b.rating  from (" \
            "SELECT rating, imdb_id from user_ratings WHERE user_id == ?)a \
                JOIN (SELECT rating, imdb_id from " \
            "user_ratings where user_id == ? )b ON a.imdb_id == b.imdb_id"

    query_for_rating = "SELECT rating from user_ratings where imdb_id == ? \
        and user_id == ?"

    c.execute(query, (user_id, int(closest_neighbour)))
    response = c.fetchall()
    # print(response)
    for movie in response:
        agreement = abs(movie[0] - movie[1]) / ((movie[0]+movie[1])/2)
        total_agreement += agreement
    total_difference = (total_agreement / len(response)) * 100
    total_agreement = 100 - total_difference
    c.execute(query_for_rating, (movie_id, int(closest_neighbour)))
    response = c.fetchone()
    if response is None:
        pass
        # print("closesnt neighbour has not seen movie")
    else:
        pass
        # print(response[0])

    # print(total_agreement)
    return


def pearson_neighbours(user_id, threshold=0.75):
    user_list = []
    neighbour_list = []
    ranked_neighbours = []
    neighbours_list_good = []
    neighbours = find_neighbours_sql(user_id)

    # query_for_users = "SELECT DISTINCT user_id from user_ratings where \
    # user_id != ? and user_id < 10"

    common_ratings_for_neighbours = "SELECT a.rating , b.rating  from (" \
        "SELECT rating, imdb_id from user_ratings WHERE user_id == ?)a JOIN \
            (SELECT rating, imdb_id from " \
        "user_ratings where user_id == ? )b ON a.imdb_id == b.imdb_id"

    for neighbour in neighbours:
        user_list = []
        neighbour_list = []
        # print(neighbour)
        c.execute(common_ratings_for_neighbours, (user_id, neighbour))
        rating_set = c.fetchall()
        for rating in rating_set:
            user_list.append(rating[0])
            neighbour_list.append(rating[1])
        if len(neighbour_list) > 2:

            corr, _ = pearsonr(user_list, neighbour_list)
            if corr > threshold:
                # print('Pearsons correlation: %.3f %.3f %.3f ' % (corr , \
                # user_id , neighbour))
                ranked_neighbours.append((corr, user_id, neighbour))
                neighbours_list_good.append(neighbour)
    # output = sorted(ranked_neighbours, key=lambda x: x[0])
    sorted(ranked_neighbours, key=lambda x: x[0])
    return neighbours_list_good


def pearson_neighbours_by_number(user_id, number=50):
    ranked_neighbours = []
    conn, c = get_db()
    neighbours_list_good = []
    neighbours = find_neighbours_sql(user_id)
    common_ratings_for_neighbours = "SELECT a.rating , b.rating  from (" \
                                    "SELECT rating, imdb_id from user_ratings \
                                        WHERE user_id == ?)a JOIN (SELECT rating, imdb_id from " \
                                    "user_ratings where user_id == ? )b ON \
                                        a.imdb_id == b.imdb_id"

    for neighbour in neighbours:
        user_list = []
        neighbour_list = []
        c.execute(common_ratings_for_neighbours, (user_id, neighbour))
        rating_set = c.fetchall()
        for rating in rating_set:
            user_list.append(rating[0])
            neighbour_list.append(rating[1])
        if len(neighbour_list) > 2:
            corr, _ = pearsonr(user_list, neighbour_list)
            if math.isnan(corr):
                corr_2 = 0
            else:
                corr_2 = corr
            ranked_neighbours.append((corr_2, user_id, neighbour))

            neighbours_list_good.append(neighbour)
    # print(ranked_neighbours)
    # sorts in place
    ranked_neighbours.sort(key=lambda tup: tup[0], reverse=True)
    # print(ranked_neighbours)
    neighbours_list_good = []
    for i in range(len(ranked_neighbours)):
        tmp_tuple = (ranked_neighbours[i][2], ranked_neighbours[i][0])
        neighbours_list_good.append(tmp_tuple)
    if len(neighbours_list_good) > number:
        # print("neighbours_list_good" + str(neighbours_list_good))
        return neighbours_list_good[:number]
    # print("ranked neighbours" + str(ranked_neighbours))
    return ranked_neighbours


if __name__ == '__main__':
    pass
    # neighbours = neighborhood_testing.find_n_neighbours(1)
    # find ratings of user
    # find ratings of all neighbours
    # neighbours = find_neighbours_sql(1)
    # get nieghbours of person 1
    # this is all users who have a movie that
    # print(find_neighbour_ratings(1,neighbours))
    # rating_of_closest_neighbour('tt0113228',1)
    # print(pearson_neighbours(1))
    # find_ratings_for_movie("tt0118798")
    # print(pearson_neighbours_by_number(1))
