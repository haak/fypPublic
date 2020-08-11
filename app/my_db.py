from app.models import Movie, Actors,  User

from app.start import get_avg_movie_score
import csv
import random
from sqlalchemy import create_engine, MetaData
# from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.expression import func, select
# import sqlite3

# THIS SEEMS TO BE LIKE SYSTEM 2 or something
# NONE OF THIS IS FROM SYSTEM 3 it wouldnt make sense. 


Base = declarative_base()
engine = create_engine('sqlite:///../db/test.db')
meta = MetaData()
Session = sessionmaker(bind=engine)
session = Session()


def fill_in_movies(file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                movie_tmp = Movie(movie_id=row[0], name=row[1])
                session.add(movie_tmp)
                session.commit()
                line_count += 1

        return


def actors_in_movies(file):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1


def pick_user_from_db():
    return
    # This should print a few users to the screen.
    # You should then be able to pick one based on id


def make_actors_db():
    query = 'insert into actor (id, actor_id, name, byear, dyear, profession) values(?, ?, ?, ?, ?, ?)'
    line_count = 0
    with open("../datasets/imdb/name.basics.tsv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            c.execute(query, (line_count, row[0], row[1], row[2], row[3], row[4]))
            line_count += 1
        conn.commit()
        conn.close()
        return


def actor_to_movie_link():
    query = 'insert into actor_to_movies (id, actor_id, movie_id) values(?, ?, ?)'
    line_count = 0
    # tmp_count = 0
    with open("../datasets/imdb/title.principals.tsv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            c.execute(query, (line_count, row[0], row[2]))
            line_count += 1
            # if line_count != 0:
            #     tmp_actor = Actors(actor_id=row[0], name=row[1], byear=row[2], dyear=row[3], profession=row[4])
            #     session.add(tmp_actor)
            #     # print(line_count)
            #     session.commit()
            #     line_count +=1
            #     tmp_count += 1
            # else:
            #     line_count += 1
            # if tmp_count > 10000:
            #     tmp_count = 0
        conn.commit()
        conn.close()
        return
        # if line_count != 0:
        #         tmp_actor_to_movie = Actor_to_Movie(movie_id=row[0],actor_id=row[2])
        #         session.add(tmp_actor_to_movie)
        #         # print(line_count)
        #
        #         line_count += 1
        #         tmp_count += 1
        #
        #     else:
        #         line_count += 1
        #
        #     if tmp_count > 1000:
        #         session.commit()
        #         tmp_count = 0
        #         # return
        #
        # return


def get_profile():
    # print("Please specify your user by id")
    # for name, id in session.query(User.name, User.id):
        # print("User: " + str(id) + " Name: " + name)
        # pass
    user_id = input("Please specify your user by id ")
    return user_id


def show_movies():
    query = "SELECT * from movies_2 WHERE movies_2.imdb_id == ?"
    query2 = "SELECT imdb_id from movies_2"
    c.execute(query2)
    id_list = c.fetchall()
    movie_list = []
    # print(session.query(Movie.id).count())
    list_of_ids = []
    # movies_count = session.query(Movie.id).count()
    for i in range(0, 6):
        # print(select.order_by(func.random()))
        rand = random.randint(0, len(id_list))
        # print(rand)
        # print(id_list)
        # print(rand)
        # print(id_list[rand])
        rand_tmp = id_list[rand]

        c.execute(query, (rand_tmp[0],))

        movie_tmp = c.fetchone()
        # print(movie_tmp)
        # movie_tmp = session.query(Movie).filter_by(id=rand).first()
        # list_of_ids.append(movie_tmp.id)
        # print(movie_tmp)
        movie_list.append(movie_tmp[0])
    return movie_list


def recommend_movie(user_id, movie_id_in):
    for movie in movie_id_in:
        actors = actors_in_movie(movie.id, user_id)
        for actor in actors:
            print(str(movie) + " has " + actor[2] + " and rating " + str(movie.rating))
        if movie.rating > 2.5:
            print(str(movie.name) + " has rating " + str(movie.rating))
    list_of_actors = []
    # session.query(User_to_Movie).filter_by(movie_id=movie_id_in).first()


def actors_in_movie(movieid, userid):

    query = """SELECT * FROM actor WHERE actor_id in
                (
                SELECT actor_id FROM actor_to_movies where imdb_id in(
                SELECT imdb_id from movie_id_to_imdb_id where movie_id in (SELECT movie_id from user_to_movie where user_id = ?)))
                AND actor_id in (
                SELECT actor_id FROM actor_to_movies where imdb_id in(
                SELECT imdb_id from movie_id_to_imdb_id where movie_id == (?)))"""
    c.execute(query, (int(userid), int(movieid)))
    return c.fetchall()


def add_rating_to_movie(movied,score):
    query = "UPDATE movies set rating = ? where movie_id = ?"
    c.execute(query, (score, movied))
    conn.commit()



def delete_table():
    # session.query(Actor_to_Movie).delete()
    # session.query(Actors).delete()
    # session.query(Movie).delete()
    # session.query(User_to_Actor).delete()
    # session.query(User_to_Movie).delete()
    # session.query(movie)
    session.commit()
    return


def create_movie_links():
    query = 'insert into movie_id_to_imdb_id (id, movie_id, imdb_id) values(?, ?, ?)'
    line_count = 0
    with open("/home/alex/Documents/fyp/datasets/ml-latest-small/links.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            c.execute(query, (line_count, row[0], "tt" + row[1]))
            line_count += 1
        conn.commit()
        conn.close()
        return


def create_movies_for_user():
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in list:
        query = "insert into user_to_movie (user_id, movie_id) VALUES (?,?)"
        c.execute(query, (1, i))
    conn.commit()
    conn.close()
    return


def create_actors_for_user():
    query = "select actor_id from actor WHERE byear = 1955"
    query1 = "insert into user_to_actor (user_id, actor_id) VALUES (?,?)"
    c.execute(query)
    # print(c.fetchall())
    for actor in c.fetchall():
        # print(actor)
        c.execute(query1, (1, actor[0]))
    conn.commit()
    conn.close()


def get_scores(movie_list):
    print(movie_list)
    list_of_movies = []
    for i in movie_list:
        # print(i)
        # print(i.movie_id)
        score = get_avg_movie_score(i.movie_id)
        i.rating = score
        list_of_movies.append(i)
        # print(score)
    return list_of_movies


# def add_ratings_to_movies():
#     query = "SELECT movie_id from movies"
#     c.execute(query)
#     for movie_id in c.fetchall():
#         print(movie_id[0])
#         score = get_avg_movie_score(movie_id[0])
#         add_rating_to_movie(movie_id[0], score)
#     conn.commit()
#     conn.close()
#     pass


def get_scores_with_sql(list_of_movies):
    list_of_movies_with_scores = []
    query = "SELECT movie_id, rating FROM movies WHERE movie_id == ?"
    for movie in list_of_movies:
        c.execute(query, movie.id)
        new_movie = c.fetchall()
        list_of_movies_with_scores.append(new_movie)
    return list_of_movies_with_scores


def run_program():
    # prints profiles that can be picked from
    # user picks a profile and the id is passed back
    # print what they have chosen.
    user = get_profile()
    # user = 1
    # print some movies they might like
    list_of_movies = show_movies()
    list_of_movies_with_scores = get_scores(list_of_movies)
    print(list_of_movies_with_scores)
    # print(list_of_movies)
    # want to move to the below function which will use sql instead.
    # list_of_movies_with_scores = get_scores_with_sql(list_of_movies)
    # print(scores)
    # user = 1
    recommend_movie(user, list_of_movies_with_scores)
    # take that list of movies and print out their review scores
    # recommend_movie(list_of_movies)
    # take that list of movies and print out any actors that are in their profiles.


def give_user_movies():
    query = "SELECT movie_id from movies "
    c.execute(query)
    ids = c.fetchall()
    query2 = "INSERT INTO user_to_movie (user_id, movie_id)  VALUES (1,?)"
    for i in range(0,100):
        c.execute(query2,  ids[random.randint(0, len(ids))])
    conn.commit()


def add_imdbid_to_movie():
    query = "SELECT movie_id from movies"
    query2 = "select imdb_id from movie_id_to_imdb_id where movie_id == ?"
    query3 = "UPDATE movies SET imdbid = ? where movie_id = ?"
    c.execute(query)
    for i in c.fetchall():
        # print(i[0])
        # print(type(i[0]))
        var = i[0]
        c.execute(query2, (i[0],))
        for imdb_id in c.fetchall():
            # print(imdb_id)
            c.execute(query3, (imdb_id[0], var))
            conn.commit()
    return


def create_objects_for_ratings():
    query = "SELECT imdbid, rating from movies"
    query2 = "INSERT into objects_info (object_id,type) VALUES (?,?)"

    c.execute(query)
    for i in c.fetchall():
        c.execute(query2)
    pass


def add_obect_to_movie():
    query = "SELECT imdbid,rating from movies"
    query2 = "INSERT INTO objects_info (movie_imdb_id,rating,type)VALUES  (?,?,?)"
    c.execute(query)
    for i in c.fetchall():
        c.execute(query2, (i[0], i[1], "rating"))
        conn.commit()
    return


def get_actors_for_movie():
    query = "SELECT actor_id from actor_to_movies WHERE imdb_id = ?"
    query2 = "INSERT INTO objects_info (movie_imdb_id,actor_imdb_id,type)VALUES  (?,?,?)"
    c.execute(query,('tt0114709',))
    for i in c.fetchall():
        c.execute(query2,('tt0114709',i[0],"actor"))
    conn.commit()


def move_actors_to_objects():
    query = "SELECT actor_id from actor"
    query2 = "SELECT MAX(object_id) FROM objects_info"
    query3 = "INSERT INTO objects_info (object_id,type) values (?,?)"
    query4 = "UPDATE actor SET object_id = ? WHERE actor_id = ?"
    c.execute(query2)
    id_number = c.fetchone()
    print(id_number)
    id_number = 0
    c.execute(query)
    for actor in c.fetchall():
        actor_id = actor[0]
        print(actor_id)
        c.execute(query3, (id_number, "actor"))
        c.execute(query4, (id_number, actor_id))
        id_number += 1
        conn.commit()
    return


if __name__ == "__main__":
    pass
    # add_rating_to_movie(1,1)
    # add_ratings_to_movies()
    run_program()
    # delete_table()
    # make_actors_db()
    # give_user_movies()
    # add_obect_to_movie()
    # get_actors_for_movie()
    # move_actors_to_objects()
