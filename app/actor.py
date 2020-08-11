import csv


class Actor:

    def __init__(self, id):
        self.name = None
        self.id = id
        self.movies = []
        self.tconst = None
        self.ordering = None
        self.nconst = None
        self.job = None
        self.characters = []
        self.category = None
        self.byear = None
        self.dyear = None

    def __str__(self):
        string = f"""Actor ID:{self.id} Name:{self.name} movies: {self.movies} \
            characters: {self.characters}"""
        return string

    def get_name(self):
        pass

    def set_name(self):
        pass

    def set_id(self):
        pass

    def get_id(self):
        pass

    def get_movies(self):
        # should return a list of movies
        return self.movies

    def set_movies(self, list_of_movies):
        self.movies = list_of_movies
        return

    def add_movie(self, movie):
        self.movies.append(movie)

    def get_name_for_actor(self):
        # print("test g")
        with open("datasets/imdb/name.basics.tsv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                # print(self.id,":",row[0])
                if self.id == row[0]:
                    self.name = row[1]
                    # print('found actros')
                    return self
