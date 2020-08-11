from enum import Enum
import omdb
import json
import sqlite3
import csv


omdb.set_default('apikey', "")
db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
conn = sqlite3.connect(db_file_desktop)
c = conn.cursor()


def get_db():
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    return conn, c


class Object_Types(Enum):
    actor = 1
    year = 2
    director = 3
    genre = 4
    plot = 5
    rated = 6
    released = 7
    runtime = 8
    writer = 9
    language = 10
    award = 11
    production = 12
    poster = 15
    country = 13
    imdb_votes = 14


# print(Types.actor.value)
# to access print(Types(1)) == Types.actor

###############################################################################
# ACTORS


def handle_actors(imdb_id, list_of_actors):
    for actor in list_of_actors:
        check = find_actor(actor)
        if check:
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.actor.value)
        else:
            insert_actor(actor)
            check = find_actor(actor)
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.actor.value)
    conn, c = get_db()
    conn.commit()
    return


def find_actor(name):
    conn, c = get_db()
    query = "SELECT object_id from actors_2 where name == ?"
    c.execute(query, (name,))
    result = c.fetchall()
    # print(result)
    if len(result) == 0:
        # print("len was 0")
        return None
    else:
        # print("else")
        return result[0]


def find_actor_by_id(object_id):
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "SELECT name from actors_2 where object_id == ?"
    c.execute(query, (object_id,))
    result = c.fetchone()
    # print(result)
    if len(result) == 0:
        # print("len was 0")
        return None
    else:
        # print("else")
        print(result[0])
        return result[0]


def insert_actor(name):
    query = "INSERT INTO actors_2 (name) VALUES (?)"
    id = find_actor(name)

    if id:
        return id
    else:
        conn, c = get_db()
        c.execute(query, (name,))
        conn.commit()
    return


def find_actor_by_imdb(imdb_actor_id):
    # will add actor_id to actors at some point.
    return


# takes in a string of actors and returns a list.
def parse_actors(str_of_actors):
    actor_list = []
    for single_actor in str_of_actors.split(","):
        actor_list.append(single_actor.strip())
    return actor_list


def print_actor(object_id):
    actor = find_actor_by_id(object_id)
    return actor

###############################################################################
# MOVIES


def find_movie(imdb_id):
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "SELECT imdb_id from movies_2 where imdb_id  == ?"
    c.execute(query, (imdb_id,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return False
    else:
        return True


def insert_movie(imdb_id, title, rating):
    query = "INSERT INTO movies_2 (imdb_id, title, rating) VALUES (?,?,?)"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    c.execute(query, (imdb_id, title, rating))
    conn.commit()
    return


def handle_movies(imdb_id, title, rating=0):
    check = find_movie(imdb_id)
    if check:
        return
    else:
        insert_movie(imdb_id, title, rating)
    return


def print_movie(imdb_id):
    query = "SELECT * from movies_2 WHERE imdb_id == ?"
    c.execute(query, (imdb_id,))
    movie = c.fetchone()
    print(movie)

###############################################################################
# MOVIE LENS USER RATING


def find_movie_lens_user_rating(imdb_id):
    query = "SELECT rating from movies_2 where imdb_id == ?"
    c.execute(query, (imdb_id,))
    if len(c.fetchall()) == 0:
        return None
    else:
        return c.fetchall()[0]


def output_rating(imdb_id):
    query = "SELECT * from movies_2 WHERE movies_2.imdb_id = ?"
    c.execute(query, (imdb_id,))
    for rating_tuple in c.fetchone():
        return "has score " + rating_tuple[0]


###############################################################################
# OLD MOVIES


def list_of_imdb_ids():
    list_of_imdb_ids_to_return = []
    query = "SELECT imdbid FROM movies WHERE imdbid not in (SELECT imdb_id \
    from movies_2)"
    c.execute(query)
    for movie in c.fetchall():
        list_of_imdb_ids_to_return.append(movie[0])
    return list_of_imdb_ids_to_return


###############################################################################
# MOVIES TO OBJECTS


def insert_into_movies_to_objects(imdb_id, object_id, type_meta):

    query = "INSERT INTO movie_to_objects (movie_id,  object_id, type) VALUES \
        (?,?,?)"
    if check_link_exists(imdb_id, object_id, type_meta):
        db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
        conn = sqlite3.connect(db_file_desktop)
        c = conn.cursor()
        # print("inserting LINK", imdb_id, object_id, type_meta)
        c.execute(query, (imdb_id, object_id, type_meta))
        conn.commit()
        return


def check_link_exists(movie_id, object_id, type_meta):
    conn, c = get_db()
    # print("checking link")
    # print(movie_id,object_id,type_meta)
    query = "SELECT movie_id from movie_to_objects where movie_id == ? AND  \
        object_id == ? and type == ?"
    c.execute(query, (movie_id, object_id, type_meta))
    result = c.fetchall()
    # print("result", result)
    if len(result) == 0:
        # should insert
        return True
    else:
        # should not insert
        return False

###############################################################################
# YEARS


def find_year(year):
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "SELECT object_id from years where year == ?"
    c.execute(query, (year,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result


def insert_year(year):
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "INSERT INTO years (year) VALUES (?)"
    c.execute(query, (year,))
    conn.commit()
    return


def handle_year(imdb_id, year):
    print(imdb_id)
    print(year)
    check = find_year(year)
    print(check)
    if check is not None:
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.year.value)
    else:
        insert_year(year)
        check = find_year(year)
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.year.value)
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    conn.commit()
    return


def print_year(object_id):
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "SELECT year from years where object_id == ?"
    c.execute(query, (object_id,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result[0]


###############################################################################
# GENRES


def find_genre(genre):
    query = "SELECT object_id from genre where genre == ?"
    conn, c = get_db()
    c.execute(query, (genre,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result


def insert_genre(genre):
    query = "INSERT INTO genre (genre) VALUES (?)"
    conn, c = get_db()
    c.execute(query, (genre,))
    conn.commit()
    return


def handle_genres(imdb_id, genre_list):

    for genre in genre_list:
        check = find_genre(genre)
        if check:
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.genre.value)
        else:
            insert_genre(genre)
            check = find_genre(genre)
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.genre.value)
    conn, c = get_db()
    conn.commit()
    return


# takes in a string of genres and returns a list.
def parse_genres(str_of_genres):
    genre_list = []
    # print(str_of_genres)
    str_of_genres_without_space = str_of_genres.replace(" ", "")
    for genre_in in str_of_genres_without_space.split(","):
        genre_list.append(genre_in)
    # print(genre_list)
    return genre_list


def print_genre(object_id):
    conn, c = get_db()
    query = "SELECT genre from genre where object_id == ?"
    c.execute(query, (object_id,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result[0]


###############################################################################
# PLOT
# insert plot


def find_plot(plot):
    query = "SELECT object_id from plot where plot == ?"
    conn, c = get_db()
    c.execute(query, (plot,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result


def insert_plot(plot):
    conn, c = get_db()
    query = "INSERT INTO plot (plot) VALUES (?)"
    c.execute(query, (plot,))
    conn.commit()
    return


def handle_plot(imdb_id, plot):
    check = find_plot(plot)
    if check:
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.plot.value)
    else:
        insert_plot(plot)
        check = find_plot(plot)
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.plot.value)
    conn, c = get_db()
    conn.commit()
    return


###############################################################################
# RELEASED


def find_relase_date(release_date):
    conn, c = get_db()
    query = "SELECT object_id from Released where Released.date == ?"
    c.execute(query, (release_date,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result


def insert_relase_date(relase_date):
    query = "INSERT INTO Released (date) VALUES (?)"
    conn, c = get_db()
    c.execute(query, (relase_date,))
    conn.commit()
    return


def handle_relase_date(imdb_id, relase_date):
    check = find_relase_date(relase_date)
    if check:
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.released.value)
    else:
        insert_relase_date(relase_date)
        check = find_relase_date(relase_date)
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.released.value)
    conn, c = get_db()
    conn.commit()
    return


###############################################################################
# RUNTIME

def find_runtime(runtime):
    conn, c = get_db()
    query = "SELECT object_id from runtime where runtime == ?"
    c.execute(query, (runtime,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result


def insert_runtime(runtime):
    conn, c = get_db()
    query = "INSERT INTO runtime (runtime) VALUES (?)"
    c.execute(query, (runtime,))
    conn.commit()
    return


def handle_runtime(imdb_id, runtime):

    check = find_runtime(runtime)
    if check:
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.runtime.value)
    else:
        insert_runtime(runtime)
        check = find_runtime(runtime)
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.runtime.value)
    conn, c = get_db()
    conn.commit()
    return


def print_runtime(object_id):
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "SELECT runtime from runtime where object_id == ?"
    c.execute(query, (object_id,))
    result = c.fetchone()

    if result is None:
        return None
    else:
        return result[0]


###############################################################################
# RATING

def find_mpaa_rating(mpaa_rating):
    query = "SELECT object_id from Rated where rating == ?"
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    c.execute(query, (mpaa_rating,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result


def insert_mpaa_rating(mpaa_rating):
    conn, c = get_db()
    query = "INSERT INTO Rated (rating) VALUES (?)"
    c.execute(query, (mpaa_rating,))
    conn.commit()
    return


def handle_mpaa_rating(imdb_id, mpaa_rating):

    check = find_mpaa_rating(mpaa_rating)
    if check:
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.rated.value)
    else:
        insert_mpaa_rating(mpaa_rating)
        check = find_mpaa_rating(mpaa_rating)
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.rated.value)
    conn, c = get_db()
    conn.commit()
    return


###############################################################################
# languages


def find_language(language):
    conn, c = get_db()
    query = "SELECT object_id from language where language == ?"
    c.execute(query, (language,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result


def insert_language(language):
    conn, c = get_db()
    query = "INSERT INTO language (language) VALUES (?)"
    c.execute(query, (language,))
    conn.commit()
    return


def handle_language(imdb_id, language_list):
    for language in language_list:
        # print("HANDLING LANGUAGES")
        check = find_language(language)
        if check:
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.language.value)
        else:
            insert_language(language)
            check = find_language(language)
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.language.value)
    conn, c = get_db()
    conn.commit()
    return


# takes in a string of genres and returns a list.
def parse_language(str_of_language):
    language_list = []
    # print(language)
    str_of_language_without_space = str_of_language.replace(" ", "")
    for genre_in in str_of_language_without_space.split(","):
        language_list.append(genre_in)
    # print(language_list)
    return language_list


def print_language(object_id):
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    query = "SELECT language from language where object_id == ?"
    c.execute(query, (object_id,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result[0]

###############################################################################
# country


def find_country(country):
    query = "SELECT object_id from country where country == ?"
    conn, c = get_db()
    c.execute(query, (country,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result


def insert_country(country):
    query = "INSERT INTO country (country) VALUES (?)"
    conn, c = get_db()
    c.execute(query, (country,))

    conn.commit()
    return


def handle_country(imdb_id, country_list):
    for country in country_list:
        check = find_country(country)
        if check:
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.country.value)
        else:
            insert_country(country)
            check = find_country(country)
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.country.value)
        conn, c = get_db()
        conn.commit()
    return


def parse_countries(str_of_countries):
    country_list = []
    str_of_countries_2 = str_of_countries.replace(" ", "")
    for country_in in str_of_countries_2.split(","):
        country_list.append(country_in)
    return country_list


def print_country(object_id):
    conn, c = get_db()
    query = "SELECT country.country from country where object_id == ?"
    c.execute(query, (object_id,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result[0]

###############################################################################
# AWARDS


def find_award(award):
    query = "SELECT object_id from awards where awards == ?"
    conn, c = get_db()
    c.execute(query, (award,))
    result = c.fetchone()
    # print("result ", result)
    if result is None:
        return None
    else:
        return result


def insert_award(award):
    conn, c = get_db()
    query = "INSERT INTO awards (awards) VALUES (?)"
    c.execute(query, (award,))
    conn.commit()
    return


def handle_award(imdb_id, award):
    check = find_award(award)
    if check:
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.award.value)
    else:
        insert_award(award)
        check = find_award(award)
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.award.value)
    conn, c = get_db()
    conn.commit()
    return


###############################################################################
# WRITERS


def handle_writers(imdb_id, list_of_writers):
    for writer in list_of_writers:
        check = find_writers(writer)
        if check:
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.writer.value)
        else:
            insert_writers(writer)
            check = find_writers(writer)
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.writer.value)
    conn, c = get_db()
    conn.commit()
    return


def find_writers(writers):
    query = "SELECT object_id from writer where writer.name == ?"
    conn, c = get_db()
    c.execute(query, (writers,))
    result = c.fetchall()
    print(result)
    if len(result) == 0:
        # print("len was 0")
        return None
    else:
        # print("else")
        return result[0]


def insert_writers(name):
    query = "INSERT INTO writer (name) VALUES (?)"
    id = find_writers(name)
    conn, c = get_db()
    if id:
        return id
    else:
        c.execute(query, (name,))
        conn.commit()
    return


# takes in a string of actors and returns a list.
def parse_writers(str_of_writer):
    writer_list = []
    for single_writer in str_of_writer.split(","):
        writer_list.append(single_writer.strip())
    return writer_list


def print_writer(object_id):
    conn, c = get_db()
    query = "SELECT writer.name from writer where object_id == ?"
    c.execute(query, (object_id,))
    result = c.fetchone()
    print(result)
    if len(result) == 0:
        # print("len was 0")
        return None
    else:
        # print("else")
        return result[0]


###############################################################################
# PRODUCTIONS


def handle_productions(imdb_id, production):
    check = find_production(production)
    if check:
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.production.value)
    else:
        insert_production(production)
        check = find_production(production)
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.production.value)
    conn, c = get_db()
    conn.commit()
    return


def find_production(production):
    conn, c = get_db()
    query = "SELECT object_id from productions where productions.name == ?"
    c.execute(query, (production,))
    result = c.fetchall()
    # print(result)
    if len(result) == 0:
        # print("len was 0")
        return None
    else:
        # print("else")
        return result[0]


def insert_production(name):
    conn, c = get_db()
    query = "INSERT INTO productions (name) VALUES (?)"
    id = find_production(name)
    if id:
        return id
    else:
        c.execute(query, (name,))
        conn.commit()
    return


def print_production(object_id):
    conn, c = get_db()
    query = "SELECT name from productions where object_id == ?"
    c.execute(query, (object_id,))
    result = c.fetchone()
    if result is None:
        return None
    else:
        # print("else")
        return result[0]

###############################################################################
# DIRECTORS


def handle_directors(imdb_id, directors):
    for director in directors:
        check = find_director(director)
        if check is not None:
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.director.value)
        else:
            insert_director(director)
            check = find_director(director)
            insert_into_movies_to_objects(imdb_id, check[0],
                                          Object_Types.director.value)
        conn, c = get_db()
        conn.commit()
    return


def handle_director_list(imdb_id, list_of_directors):
    for director in list_of_directors:
        handle_directors(imdb_id, director)



def find_director(name):
    print(name)
    query = "SELECT object_id from director where name == ?"
    conn, c = get_db()
    c.execute(query, (name,))
    result = c.fetchall()
    # print(result)
    if len(result) == 0:
        # print(result)
        # print("len was 0")
        # print("  \n\n\n\n\n")
        return None
    else:
        print("else \n\n\n\n")
        return result[0]


def insert_director(name):
    query = "INSERT INTO director (name) VALUES (?)"
    id = find_director(name)
    if id:
        return id
    else:
        conn, c = get_db()
        c.execute(query, (name,))
        conn.commit()
    return


# takes in a string of actors and returns a list.
def parse_directors(str_of_directors):
    # str_of_directors = "Allison Anders, Alexandre Rockwell, Robert Rodriguez,
    #  Quentin Tarantino"
    director_list = []
    # str_of_directors_2 = str_of_directors.replace(" ", "")
    for single_director in str_of_directors.split(","):
        director_list.append(single_director.strip())
    return director_list


def find_director_by_id(object_id):
    conn, c = get_db()
    query = "SELECT name from director where object_id == ?"
    c.execute(query, (object_id,))
    result = c.fetchone()
    # print(result)
    if len(result) == 0:
        # print("len was 0")
        return None
    else:
        # print("else")
        return result[0]


def print_director(object_id):
    return find_director_by_id(object_id)

###############################################################################
# Poster links


def handle_posters(imdb_id, poster):
    check = find_poster(poster)
    if check:
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.poster.value)
    else:
        insert_poster(poster)
        check = find_poster(poster)
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.poster.value)
    conn, c = get_db()
    conn.commit()
    return



def find_poster(link):
    query = "SELECT object_id from posters where link == ?"
    print("trying to find poster \n\n\n\n\n")
    conn, c = get_db()
    c.execute(query, (link,))
    result = c.fetchall()
    print(result)

    if len(result) == 0:
        print("len was 0")
        return None
    else:
        print("else")
        return result[0]


def insert_poster(link):
    print(link)
    query = "INSERT INTO posters (link) VALUES (?)"
    id = find_poster(link)
    if id:
        return id
    else:

        conn, c = get_db()
        c.execute(query, (link,))
        conn.commit()
    return


###############################################################################
# IMDB VOTES

def handle_imdb_votes(imdb_id, imdb_votes):
    check = find_imdb_votes(imdb_votes)
    if check:
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.imdb_votes.value)
    else:
        insert_imdb_votes(imdb_votes)
        check = find_imdb_votes(imdb_votes)
        insert_into_movies_to_objects(imdb_id, check[0],
                                      Object_Types.imdb_votes.value)
    conn, c = get_db()
    conn.commit()
    return


def find_imdb_votes(imdb_votes):
    query = "SELECT object_id from imdb_votes where votes == ?"
    conn, c = get_db()
    c.execute(query, (imdb_votes,))
    result = c.fetchall()
    # print(result)
    if len(result) == 0:
        # print("len was 0")
        return None
    else:
        # print("else")
        return result[0]


def insert_imdb_votes(imdb_votes):
    query = "INSERT INTO imdb_votes (votes) VALUES (?)"
    id = find_imdb_votes(imdb_votes)
    if id:
        return id
    else:
        conn, c = get_db()
        c.execute(query, (imdb_votes,))
        conn.commit()
    return


def parse_imdb_votes(str_of_imdb_votes):
    # print(str_of_imdb_votes)
    if str_of_imdb_votes == 'N/A':
        return 0
    else:
        imdb_votes = str_of_imdb_votes.replace(",", "")
        return int(imdb_votes)


###############################################################################
# OMDB



def scrape_omdb():
    movies_to_scrape = list_of_imdb_ids()
    current = 0
    for movie in movies_to_scrape:
        if current > 20:
            return
        scrape_omdb_response = json_for_movie(movie)
        filter_movie(scrape_omdb_response)
        current += 1
        # print("test")

    return


def scrape_omdb_with_movie_id(imdb_id):
    response = json_for_movie(imdb_id)
    filter_movie(response)
    return


# def clear_db():

#     query = "DELETE FROM movie_to_objects"
#     c.execute(query)
#     query = "DELETE FROM actors_2"
#     c.execute(query)
#     query = "DELETE FROM genre"
#     c.execute(query)
#     query = "DELETE FROM plot"
#     c.execute(query)
#     query = "DELETE FROM writer"
#     c.execute(query)
#     query = "DELETE FROM director"
#     c.execute(query)
#     query = "DELETE FROM parsed_imdb"
#     c.execute(query)
#     query = "DELETE FROM unparsed_imdb"
#     c.execute(query)
#     query = "DELETE FROM awards"
#     c.execute(query)
#     query = "DELETE FROM director"
#     c.execute(query)
#     query = "DELETE FROM imdb_votes"
#     c.execute(query)
#     query = "DELETE FROM language"
#     c.execute(query)
#     query = "DELETE FROM movies_2"
#     c.execute(query)
#     query = "DELETE FROM country"
#     c.execute(query)
#     query = "DELETE FROM posters"
#     c.execute(query)
#     query = "DELETE FROM productions"
#     c.execute(query)
#     query = "DELETE FROM Rated"
#     c.execute(query)
#     query = "DELETE FROM Released"
#     c.execute(query)
#     query = "DELETE FROM runtime"
#     c.execute(query)
#     query = "DELETE FROM years"
#     c.execute(query)
#     conn.commit()


def json_for_movie(imdb_id):
    response = omdb.imdbid(imdb_id)
    return response


def write_parsed_to_file(json_request):
    write_parsed_or_unparsed_to_file(json_request, "parsed_imdb")


def write_non_parsed_to_file(json_request):
    write_parsed_or_unparsed_to_file(json_request, "unparsed_imdb")


def write_parsed_or_unparsed_to_file(json_request, type_of_parse):
    f = open("/home/alex/Documents/fyp/datasets/omdb/scrape.txt", "a")
    json.dump(json_request, f)
    conn, c = get_db()
    f.write("\n")
    select_query = "SELECT {} from {} WHERE {} == ?".format("imdb_id",
                                                            type_of_parse,
                                                            "imdb_id")
    c.execute(select_query, (json_request["imdb_id"],))
    if not c.fetchone():
        query = "INSERT INTO {} {} VALUES (?)".format(type_of_parse,
                                                      "(imdb_id)")
        imdb_id = json_request["imdb_id"]

        c.execute(query, (imdb_id,))
        conn.commit()


def read_in_from_file():
    f = open("/home/alex/Documents/fyp/datasets/omdb/scrape.txt", "r")
    for line in f:
        response = line
        # print(response)
        filter_movie(response)
    return


def filter_movie(json_for_movie):
    if type(json_for_movie) == str:
        response = eval(json_for_movie)
    else:
        response = json_for_movie
    movie = response["imdb_id"]
    imdb_votes_str = response["imdb_votes"]
    imdb_votes = parse_imdb_votes(imdb_votes_str)
    if imdb_votes >= 0:
        title = response['title']
        handle_movies(movie, title)

        year = response["year"]
        handle_year(movie, year)

        rated = response["rated"]
        handle_mpaa_rating(movie, rated)

        released = response["released"]

        handle_relase_date(movie, released)

        runtime = response["runtime"]
        # print(runtime)
        handle_runtime(movie, runtime)

        genre = response["genre"]
        genre_list = parse_genres(genre)
        handle_genres(movie, genre_list)

        director = response["director"]
        # print(director)
        director_list = parse_directors(director)
        handle_directors(movie, director_list)

        writers = response["writer"]
        list_of_writers = parse_writers(writers)
        handle_writers(movie, list_of_writers)

        actors = response["actors"]
        parsed_actors = parse_actors(actors)
        handle_actors(movie, parsed_actors)

        plot = response["plot"]
        handle_plot(movie, plot)

        languages = response["language"]
        languages_list = parse_language(languages)
        # print("lang_list", languages_list)
        handle_language(movie, languages_list)

        country = response["country"]
        country_list = parse_countries(country)
        handle_country(movie, country_list)

        awards = response["awards"]
        handle_award(movie, awards)

        poster_link = response["poster"]
        handle_posters(movie, poster_link)

        # print(response)
        production = response["production"]
        handle_productions(movie, production)

        handle_imdb_votes(movie, imdb_votes)
        # print("parsed movie" + movie)
        write_parsed_to_file(response)
        return 1

    else:
        # print('imdb less than 1000')
        write_non_parsed_to_file(response)
        return 0


def get_ratings():
    query = "SELECT imdbid,rating FROM movies"
    query2 = "UPDATE movies_2 set rating = ? WHERE imdb_id = ?"
    c.execute(query)
    for movie in c.fetchall():
        # print(movie)
        c.execute(query2, (movie[1], movie[0]))
        conn.commit()
    return


def compare_movie(imdb_id, user_id):
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()

    query2 = """
    SELECT  t1.type, t1.object_id , COUNT(*)FROM (
    (SELECT movie_id,type,object_id FROM movie_to_objects
    WHERE movie_id == ?) t1
    LEFT JOIN
    (SELECT movie_id, type, object_id FROM movie_to_objects  GROUP BY
    object_id, type , movie_id HAVING movie_id in (SELECT imdb_id FROM
    movie_id_to_imdb_id
     WHERE imdb_id in (SELECT user_ratings.imdb_id FROM user_ratings WHERE
     user_id == ?))
    ) t2 on t1.object_id = t2.object_id AND t1.type = t2.type) GROUP BY
    t1.type, t1.object_id ORDER BY t1.type;
    """

    c.execute(query2, (str(imdb_id), int(user_id)))
    result = c.fetchall()

    return result


# def run_program_2():
#     user = my_db.get_profile()
#     movie_list = my_db.show_movies()
#     for movie in movie_list:
#         # print_movie(movie)
#         # print(user,movie)
#         # print(type(user))
#         # print(type(movie))
#         explanation_list = compare_movie(movie, int(user))
#         for explanation in explanation_list:
#             # print_thing(explanation)
#             pass
#     # print(movie_list)


def print_thing(movie_in):
    # print(movie_in)
    # movie_type = movie_in[0]
    # movie_id = movie_in[1]
    # movie_count  = movie_in[2]
    # print("type {} Id: {} has appeared {} many times ".format(movie_type,
    # movie_id, movie_count))
    # print("type {} ID: {} has appeared {} time/s".format(Types(movie_type)
    # movie_id,movie_count))
    return


def read_in_movie_lens():
    line_count = 0
    with open("/home/alex/Documents/fyp/datasets/ml-latest-small/links.csv") as csv_file:  # noqa: E501
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count != 0:
                imdb_id = "tt" + row[1]
                scrape_omdb_with_movie_id(imdb_id)
            line_count += 1
    return


def has_movie_been_scraped(imdb_id):
    if find_movie(imdb_id) is False:
        return False
    else:
        return True


def print_explanation(type_id, object_id, count):
    # "object type , object id , count"
    list_of_types = [1, 2, 3, 4, 8, 9, 10, 12, 13]
    output = ""
    # print(type_id,object_id)
    output += find_object(type_id, object_id)
    if type_id in list_of_types:
        if count == 1:
            tmp_output = " appears " + str(count) + " time in your profile"
        else:
            tmp_output = " appears " + str(count) + " times in your profile"
        output += tmp_output
        return output
    else:
        return ""


def find_object(type_num, object_id):
    if type_num == 1:
        actor = print_actor(object_id)
        return "actor " + actor
    elif type_num == 2:
        year = print_year(object_id)
        return "The year " + str(year)
    elif type_num == 3:
        director = print_director(object_id)
        return "The director " + str(director)
    elif type_num == 4:
        genre = print_genre(object_id)
        return "The genre " + str(genre)
    elif type_num == 8:
        runtime = print_runtime(object_id)
        return "The runtime " + str(runtime)
    elif type_num == 9:
        writer = print_writer(object_id)
        return "The writer " + str(writer)
    elif type_num == 10:
        language = print_language(object_id)
        return "The language " + str(language)
    elif type_num == 12:
        production = print_production(object_id)
        return "The Production " + str(production)
    elif type_num == 13:
        country = print_country(object_id)
        return "The Country " + str(country)
    else:
        return ""


def get_db():
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    return conn, c


def get_un_scraped_movies():
    query = "SELECT DISTINCT imdb_id from user_ratings where imdb_id not in (SELECT  imdb_id from movies_2)"
    conn, c = get_db()
    c.execute(query)
    
    result = c.fetchall()
    for movie in result:
        print(movie)
        scrape_omdb_with_movie_id(movie[0])
        conn.commit()
        return


if __name__ == '__main__':
    pass
