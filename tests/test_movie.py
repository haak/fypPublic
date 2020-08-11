# from app.scrape_omni import run
from app.omdb_test import handle_year

from app.omdb_test import insert_director
from app.omdb_test import json_for_movie, filter_movie
from app.movie_lens_methods import pearson_neighbours_by_number


def test_run():
    return


imdb_id = "tt3794354"
year = 2020


def test_handle_year():
    handle_year(imdb_id, year)
    print()


name = "Adil El Arbi"


def test_insert_director():
    insert_director(name)


def test_scrape_movie():
    response = json_for_movie("tt6673612")
    filter_movie(response)
    return


def test_pearson():
    result = pearson_neighbours_by_number(1)
    print(result)


if __name__ == '__main__':
    # test_handle_year()
    # test_insert_director()
    # test_scrape_movie()
    test_pearson()
    pass
