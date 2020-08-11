#!/usr/bin/env python3
import csv
import random
from app.movie import Movie
from app.actor import Actor


def return_random_number(bottom, top):
    return random.randint(bottom, top)


def find_random_id_from_list(list_of_movie_ids, number):
    list_of_random_ids = []
    list_of_random_ids2 = []
    for i in range(0, number):
        list_of_random_ids.append(random.randint(1, len(list_of_movie_ids)))

    for i in list_of_random_ids:
        list_of_random_ids2.append(list_of_movie_ids[i])
    return list_of_random_ids2


def find_random_movie(id, file):
    list_of_movie_ids = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if list_of_movie_ids[id] == row[0]:
                print(f'id:{row[0]} Title: {row[1]} genre: {row[2]}.')
                return
            list_of_movie_ids.append(row[0])
            line_count += 1
    return


def read_in_movies(file):
    list_of_movie_ids = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            # skip first line.
            if line_count == 0:
                line_count += 1
            else:
                list_of_movie_ids.append(row[0])
                line_count += 1
        return list_of_movie_ids


def get_avg_movie_score(movie_id):
    score = 0
    total_movies = 0
    linecount = 0
    with open("/home/alex/Documents/fyp/datasets/ml-latest-small/ratings.csv") as ratings:
        csv_reader1 = csv.reader(ratings, delimiter=",")
        for row in csv_reader1:
            # print("score: ", score, "total_movies: ", total_movies)

            if linecount == 0:
                linecount += 1
                continue
            else:
                # print(row[1])
                # print(movieID)
                if int(row[1]) == int(movie_id):
                    score += float(row[2])
                    total_movies += 1
                linecount += 1
        if score == 0 and total_movies == 0:
            # print("score: ", score, "total_movies: ", total_movies)
            return 0
        return score/total_movies


def get_movie_title(MovieObject):
    linecount = 0
    with open("ml-latest-small/movies.csv") as csv_file:
        # print("help")
        # print(MovieObject.id)
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if linecount == 0:
                linecount += 1
                continue
            else:
                if int(MovieObject.id) == int(row[0]):
                    # print(MovieObject.id)
                    MovieObject.name = row[1]
                    return MovieObject
    return MovieObject


def get_actors_for_movies(MovieObject):
    return


def create_movie_objects():
    linecount = 0
    list_of_movies = []
    with open("ml-latest-small/movies.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if linecount == 0:
                linecount += 1
                continue
            else:
                if linecount < 100:
                    movie = Movie(row[0], row[1], row[2])
                    list_of_movies.append(movie)        
                    linecount += 1
        return list_of_movies


def create_actor_from_movie(movie):
    list_of_actors = []
    for i in movie.actors:
        actor = Actor(i[2])
        actor.movies.append(movie.name)
        actor.category = i[3]
        actor.job = i[4]
        actor.characters = i[5]
        list_of_actors.append(actor)
    return list_of_actors

def create_movie_object():
    linecount = 0
    list_of_movies = []
    with open("ml-latest-small/movies.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if linecount == 0:
                linecount += 1
                continue
            else:
                if linecount < 2:
                    movie = Movie(row[0], row[1], row[2])
                    list_of_movies.append(movie)        
                    linecount += 1
                    return movie



def main():
    movies = []
    # main function to be run.
    # get list of movid ids
    file = "ml-latest-small/movies.csv"
    list_of_movie_ids = read_in_movies(file)
    numbers = find_random_id_from_list(list_of_movie_ids, 5)
    scores = []
    # print(numbers)
    for i in numbers:
        score = get_avg_movie_score(i)
        # im rounding to 1 decimal place.
        roundedScore = round(score, 1)
        scores.append(score)
        # should add the name here.
        movie_tmp = Movie(i, "", "", roundedScore)
        movie_tmp = get_movie_title(movie_tmp)
        movies.append(movie_tmp)

    for i in movies:

        # movie1 = create_movie_object()
        i.get_imdb_id()
        i.get_actors_for_movie()
        print(i)
        # print(movie1.actors)
        actors = create_actor_from_movie(i)
        for i in actors:
            i.get_name_for_actor()
            print(i)
        print("\n")

    # pick 3 random ones
    # create movie objects
    # get ratings for each of those movies.
    # print movie title, rating and the total number of ratings.
    # get dataset with actors in it
    # get main actors in the filem.
    # print them with the name of the film.
    return


if __name__ == "__main__":

    # main()
    print("hello and welcome to the movie recommender")
    print("please pick a person")
    #for i in person:
    print("print out people you can pick from here")
    print("this should pull from the db table of all users. ")




    # movie1 = create_movie_object()
    # movie1.get_imdb_id()
    # movie1.get_actors_for_movie()
    # # print(movie1.actors)
    # actors = create_actor_from_movie(movie1)
    
    # for i in actors:
    #     i.get_name_for_actor()
        
    #     print(i)
    
        






# with open('data.txt', 'w') as outfile:
    # json.dump(data, outfile)
