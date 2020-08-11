import random
from enum import Enum
from app.omdb_test import print_explanation
import jsonpickle
import sqlite3

RANDOM_SCORING = 0
movie_title_and_poster = 0


def get_db():
    db_file_desktop = "/home/alex/Documents/fyp/db/test.db"
    conn = sqlite3.connect(db_file_desktop)
    c = conn.cursor()
    return conn, c


def get_object_from_json(json_object):
    self_thawed = jsonpickle.decode(json_object)
    return self_thawed


# takes in a triple of (explanation_type,object_id,count)
def get_explanation(explanation_triple, imdb_id, user_id, settings):

    movie_title_and_poster = settings[1]
    random_explanations = settings[2]
    
    tmp_explanation = Explanation()
    tmp_explanation.user_id = user_id
    tmp_explanation.explanation_type = explanation_triple[0]
    tmp_explanation.object_id = explanation_triple[1]
    tmp_explanation.count = explanation_triple[2]
    tmp_explanation.imdb_id = imdb_id
    movie_title = get_movie_name_from_id(imdb_id)
    if movie_title_and_poster == 1:
        tmp_explanation.explanation = movie_title + " : "
    else:
        tmp_explanation.explanation = ""
    tmp_explanation.explanation += print_explanation(explanation_triple[0],
                                                     explanation_triple[1],
                                                     explanation_triple[2])
    if random_explanations == 1:
        tmp_explanation.get_random_rating()
    else:
        tmp_explanation.get_rating_for_explanation()
        
    tmp_explanation.explanation += " "
    # tmp_explanation.explanation += str(tmp_explanation.rating)

    # print(tmp_explanation.explanation)

    # print("\n\n\n\n\n\n")
    # print(tmp_explanation.rating)
    # add title to explanation at the start

    return tmp_explanation


class Explanation:
    def __init__(self):
        # text to print to screen
        self.explanation = None
        # ratings should be values between -1 and 1
        self.rating = 0
        # types like actor or poster or something
        self.explanation_type = None
        self.object_id = None
        
        # if its metadata number of times an actor shows up.
        self.count = None
        self.user_id = None
        self.imdb_id = None

    def get_rating(self):
        return self.rating

    def set_explanation(self, explanation):
        self.explanation = explanation
        return

    def set_rating(self, rating):
        self.rating = rating
        return

    def rank_explanation(self):
        # this should change the rating of the explanation based on the type
        # and value
        # different types will have different good values
        return

    def get_object_id(self):
        return self.object_id

    def get_object_string(self):
        # object type , object id , count
        self.explanation = print_explanation(self.explanation_type,
                                             self.object_id,
                                             self.count)

    def get_random_rating(self):
        self.rating = random.randint(0, 100)/100

    def get_json_for_object(self):
        self_frozen = jsonpickle.encode(self)
        return self_frozen

    def get_rating_for_explanation(self):
        if RANDOM_SCORING:
            self.rating = random.randint(0, 100)/100
        else:
            # self.rating = 0
            if self.explanation_type == 1:
                # actor
                # print("getting score for type 1")
                score = self.get_score_for_type()
                # print("got score for type 1")
                # print(score)
                self.rating = score + 0.5
                # self.rating == "HIGH if low"

            elif self.explanation_type == 2:
                # year
                score = self.get_score_for_type()
                self.rating = score
                # self.rating = "high if high"
            elif self.explanation_type == 3:
                score = self.get_score_for_type()
                self.rating = score
                # director
                # self.rating = "high if high"
            elif self.explanation_type == 4:
                score = self.get_score_for_type()
                self.rating = score
                # genre
                # self.rating = "high if high"
            elif self.explanation_type == 5:
                # score = self.get_score_for_type(5)
                # self.rating = score
                # plot
                self.rating = 0
            elif self.explanation_type == 6:
                score = self.get_score_for_type()
                self.rating = score
                # rated
                # self.rating = "high if high"
            elif self.explanation_type == 7:
                score = self.get_score_for_type()
                self.rating = score
                # released
                self.rating = 0
            elif self.explanation_type == 8:
                score = self.get_score_for_type()
                self.rating = score
                # runtime
                # self.rating = "2 categories longer than 2 hours less
                # than 2 hours."
            elif self.explanation_type == 9:
                score = self.get_score_for_type()
                self.rating = 1 - score
                # writer
                # self.rating = "high if high"
            elif self.explanation_type == 10:
                score = self.get_score_for_type()
                self.rating = score
                # language
                # self.rating = "high if low"
            elif self.explanation_type == 11:
                score = self.get_score_for_type()
                self.rating = 1 - score
                # award
                self.rating = 0
            elif self.explanation_type == 12:
                score = self.get_score_for_type()
                self.rating = score
                # production
                # self.rating = "wont be used"
            elif self.explanation_type == 13:
                score = self.get_score_for_type()
                self.rating = score
                # country
                # self.rating = "high if low"
            elif self.explanation_type == 14:
                score = self.get_score_for_type()
                self.rating = score
                # imdb votes
                # self.rating = "high if high"
            elif self.explanation_type == 15:
                # score = self.get_score_for_type(15)
                # self.rating = score
                # poster
                self.rating = 0
            else:
                
                print("\n\n\n\n\n\n")
                print("going to the else")
                print("\n\n\n\n\n\n")
                self.rating = 0
            if self.count == 1:
                self.rating = 0

  
        #
        return

    def get_score_for_type(self):
        # type_dict = {1: "actors_2", 2: "year", 3: "director", 4: "genre",
        #  5: "plot", 6: "Rated", 7: "released",
        #  8: "runtime", 9: "writer", 10: "language",
        #  11: "award", 12: "production", 13: "country",
        #  14: "imdb_votes", 15: "posters"}

        max_for_type = get_max_for_type(self.explanation_type)
        min_for_type = get_min_for_type(self.explanation_type)
        normal = (self.count - min_for_type) / (max_for_type - min_for_type)
        return normal

    def get_dictionary_for_object(self):
        tmp_dict = {}
        if self.count:
            tmp_dict["count"] = self.count
        if self.rating:
            tmp_dict["expr_rating"] = self.rating
        if self.explanation:
            tmp_dict["explanation"] = self.explanation
        if self.explanation_type:
            tmp_dict["explanation_type"] = self.explanation_type
        if self.imdb_id:
            tmp_dict["imdb_id"] = self.imdb_id
        if self.object_id:
            tmp_dict["object_id"] = self.object_id
        return tmp_dict

    def write_explanation_to_db(self):
        conn, c = get_db()
        query = "INSERT INTO explanations(user_id, imdb_id, count, type, object_id, \
            explanation_string, rating) VALUES(?, ?, ?, ?, ?, ?, ?);"
        c.execute(query, (self.user_id, self.imdb_id, self.count,
                          self.explanation_type, self.object_id,
                          self.explanation,
                          self.rating))
        # result = c.fetchall()
        conn.commit()
        conn.close()
        return


class ExplanationType(Enum):
    actor = 1
    year = 2
    director = 3
    genre = 4
    rated = 6
    released = 7
    runtime = 8
    writer = 9
    language = 10
    award = 11
    production = 12
    country = 13


def read_explanation_from_db(user_id, imdb_id, debate_round):
    conn, c = get_db()
    query = "SELECT * from explanations where user_id == ? and imdb_id == ? \
         ORDER BY  rating desc LIMIT ?;"
    c.execute(query, (user_id, imdb_id, debate_round))
    result = c.fetchall()
    # print(result)
    return result


def read_explanation_from_db_for_user(user_id, debate_round):
    conn, c = get_db()
    query = "SELECT * from explanations where user_id == ?  \
         ORDER BY rating asc LIMIT ?;"
    c.execute(query, (user_id, debate_round))
    result = c.fetchall()
    return result

def create_explanation_list(user_id, imdb_id, debate_round):
    explanation_list = []
    explantions = read_explanation_from_db(user_id, imdb_id, debate_round)
    for explantion in explantions:
        explanation_list.append(explantion)
    return explanation_list


def get_max_for_type(object_type):
    conn, c = get_db()
    query = """SELECT count from (
SELECT  t1.type, t1.object_id , COUNT(*) as count FROM (
    (SELECT movie_id, type, object_id FROM movie_to_objects
    WHERE type == ?) t1
    LEFT JOIN

    (SELECT movie_id, type, object_id FROM movie_to_objects  GROUP BY
    object_id, type , movie_id
    )
        t2 on t1.object_id = t2.object_id AND t1.type = t2.type)
GROUP BY
    t1.type, t1.object_id ORDER BY t1.type) as counts order by count
    DESC LIMIT 1;"""
    c.execute(query, (object_type,))
    result = c.fetchone()
    return result[0]


def get_min_for_type(object_type):
    conn, c = get_db()
    query = """SELECT count from (
SELECT  t1.type, t1.object_id , COUNT(*) as count FROM (
    (SELECT movie_id, type, object_id FROM movie_to_objects
    WHERE type == ?) t1
    LEFT JOIN

    (SELECT movie_id, type, object_id FROM movie_to_objects  GROUP BY
    object_id, type , movie_id
    )
        t2 on t1.object_id = t2.object_id AND t1.type = t2.type)
GROUP BY
    t1.type, t1.object_id ORDER BY t1.type) as counts order by count
     LIMIT 1;"""
    c.execute(query, (object_type,))
    result = c.fetchone()
    return result[0]


def get_movie_name_from_id(imdb_id):
    conn, c = get_db()
    query = "SELECT  title from movies_2 where imdb_id == ?"
    c.execute(query, (imdb_id,))
    result = c.fetchone()
    return result[0]


def create_explanation_from_db(debate_round, user_id, imdb_id):
    movie_explanations = []
    explanation_list = create_explanation_list(user_id, imdb_id, debate_round)
    for explanation in explanation_list:

        tmp_explanation = Explanation()

        tmp_explanation.user_id = explanation[1]
        tmp_explanation.imdb_id = explanation[2]
        tmp_explanation.count = explanation[3]
        tmp_explanation.explanation_type = explanation[4]
        tmp_explanation.object_id = explanation[5]
        tmp_explanation.explanation = explanation[6]
        tmp_explanation.rating = explanation[7]
        tmp_dict = tmp_explanation.get_dictionary_for_object()
        movie_explanations.append(tmp_dict)
        
    return movie_explanations


def get_explanations_for_user(debate_round, user_id):
    movie_explanations = []
    explanation_list = read_explanation_from_db_for_user(
        user_id, debate_round)
    for explanation in explanation_list:

        tmp_explanation = Explanation()

        tmp_explanation.user_id = explanation[1]
        tmp_explanation.imdb_id = explanation[2]
        tmp_explanation.count = explanation[3]
        tmp_explanation.explanation_type = explanation[4]
        tmp_explanation.object_id = explanation[5]
        tmp_explanation.explanation = explanation[6]
        tmp_explanation.rating = explanation[7]
        tmp_dict = tmp_explanation.get_dictionary_for_object()
        movie_explanations.append(tmp_dict)

    return movie_explanations


