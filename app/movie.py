import csv
import sqlite3
conn = sqlite3.connect("/home/alex/Documents/fyp/db/test.db")
c = conn.cursor()


class Movie:
    def __init__(self, id="###", name="###", genres="###", rating="###"):
        self.id = id
        self.name = name
        self.genres = genres
        self.rating = rating
        self.actors = []
        self.ImdbId = None

    def __str__(self):
        # returns a string to be printed
        string = f"""Movie ID:{self.id}
Name:{self.name}
rating: {self.rating}
genres: {self.genres}
imdbID: {self.ImdbId}
"""
        return string

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_name(self, name):
        self.name = name
        return

    def get_name(self):
        return self.name

    def get_imdb_id(self):
        linecount = 0
        with open("ml-latest-small/links.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if linecount == 0:
                    linecount += 1
                else:
                    if int(self.id) >= int(row[0]):
                        if int(self.id) == int(row[0]):
                            # print(row[1])
                            self.ImdbId = "tt" + row[1]
                            # print(self.ImdbId)
                            break
                    else:
                        break

    def get_actors_for_movie(self):
        found_group = 0
        with open("datasets/imdb/title.principals.tsv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                if self.ImdbId == row[0]:

                    # print("found it")
                    # print(row)
                    self.actors.append(row)
                    found_group = 1
                elif found_group == 1:
                    return
            return

            pass


# def output_movie_score(imdb_id):
#     query = "SELECT rating from movies WHERE imdbid = ?"
#     c.execute(query, (imdb_id,))
#     return c.fetchone()
