import omdb
import requests
from bs4 import BeautifulSoup
from ast import literal_eval
# from app import debate
# from app.debate import get_movies_based_on_pearson


def get_omniplex_movies():
    banned_movies = []
    # banned_movies = ['365 dni', 'Ladies and Gentlemen, the Fabulous Stains',
    #                  'Agrippina (Handel) -LIVE - from Met Opera', "Agrippina
    # (Handel) -LIVE - from Met Opera",
    #                  "Andre Rieu 2020 Maastricht Concert Happy Together",
    #                  "Andre Rieu 2020 Maastricht Concert Happy Together
    # (Encore)",
    #                  "Cavalleria Rusticana/Pagliacci - LIVE - Royal Opera",
    #                  "Cellist, The/ Dances at a Gathering - LIVE - Royal
    # Ballet",
    #                  "Cherry Orchard, The",
    #                  "Comedy of Errors, The - LIVE from RSC",
    #                  "Cyrano De Bergerac - LIVE from National Theatre (ROI)",
    #                  "Dante Project, The (World Premiere) - LIVE - Royal
    # Ballet",
    #                  "David Attenborough: A Life on Our Planet - Live From
    # the World Premiere",
    #                  "Der Fliegende Hollander (Wagner) - LIVE - from Met
    # Opera"]

    movies_list = ["bad boys for life", "Bombshell", "The call of the wild",
                   "Onward", "Dolittle", "Birds of prey", "Sonic the hedgehog"]
    # movies_list = ["iron man", "iron man 2", ""]

    # url = "https://www.omniplex.ie/engine/ajax.php"
    url = ""
    # data = "requestType=quickBookMovies&siteCode=OMP_MAHO"
    data = ""

    
    # mydict ={'Host': 'www.omniplex.ie', "User-Agent": "Mozilla/5.0 (X11; \
    # Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0","Accept": \
    # "*/*",
    # "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, \
    # br", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    # "X-Requested-With": "XMLHttpRequest",  "Content-Length": "45",
    # "Origin": "https://www.omniplex.ie",    "Connection": "keep-alive",
    # "Referer": "https://www.omniplex.ie/cinema/cork-mahon-point", "Cookie": \
    # "__cfduid=dc9aa9e0a5a08217beb4accb5f186b9331570285346; \
    # cc_cookie_accept=cc_cookie_accept; sitecode=OMP_MAHO; \
    # cc_cookie_decline=null; currentViewDate=04-11-2019; \
    # PHPSESSID=pvqdhk5a01cr9r6lkgfr19v3u0; __cflb=2033366282",
    # "TE": "Trailers", "Pragma": "no-cache", "Cache-Control": "no-cache"}

    mydict = {}

    response = requests.post(url, data=data, headers=mydict)
    soup = BeautifulSoup(response.text, features="html.parser")
    movies = soup.findAll("option")

    for movie in movies[1:]:
        print(movie.text)
        # once in a while
        if movie.text != "Choose Movie" and movie.text not in banned_movies:
            movies_list.append(movie.text)
    return movies_list


def get_omniplex_movies_static():

    movies_list = ["Sonic the Hedgehog", "My spy",
                   "Onward", "Invisible man", "Bloodshot", "the call of the wild", "1917"]
    return movies_list


def write_movies_to_file(movies):
    with open("sample.txt", "a") as movies_file:
        movies_file.write(str(movies))
        movies_file.write("\n")


def get_json_for_title(title):
    omdb.set_default('apikey', "")
    res = omdb.request(y="2020", t=title)
    if res.text != '{"Response":"False","Error":"Movie not found!"}':
        try:
            # write_movies_to_file(res.text)
            return res.text
        except TypeError:
            return False
    else:
        return False


def get_json_for_imdb(imdb_id):
    omdb.set_default('apikey', "")
    res = omdb.request(i=imdb_id)
    if res.text != '{"Response":"False","Error":"Movie not found!"}':
        try:
            # write_movies_to_file(res.text)
            return res.text
        except TypeError:
            return False
    else:
        return False


def get_poster_for_movie(movie_dict):
    # print("getting movie poster")
    # print(movie_dict)
    path = "/home/alex/Documents/fyp/app/static/"
    if movie_dict == {'Response': 'False', 'Error': 'Movie not found!'} or \
       movie_dict["Poster"] == 'N/A':
        return None

    url = movie_dict["Poster"]
    filename = url.split('/')[-1]
    r = requests.get(url, allow_redirects=True)
    open(path+filename, 'wb').write(r.content)


def run():
    movies_jsons = []
    omdb.set_default('apikey', "")
    # movies = get_omniplex_movies()
    movies = get_omniplex_movies_static()
    for movie in movies:
        movie_json = get_json_for_title(movie)
        if movie_json is not False:
            movie_dict = literal_eval(movie_json)
            get_poster_for_movie(movie_dict)
            movies_jsons.append(movie_dict)
    return movies_jsons


# def run_pearson(user_id):
#     movies_jsons = []
#     omdb.set_default('apikey', "")
#     # movies = get_omniplex_movies()
#     print("userid")
#     print(user_id)
#     movies = get_movies_based_on_pearson(user_id)
#     print("movies that are in run_pearson")
#     for movie in movies:
#         movie_json = get_json_for_imdb(movie[1])
#         print("\n\n\n\n\n\n")
#         print("movie_json")
#         print(movie_json)
#         print("\n\n\n\n\n\n")
#         if movie_json is not False:
#             movie_dict = literal_eval(movie_json)
#             get_poster_for_movie(movie_dict)
#             movies_jsons.append(movie_dict)
#     return movies_jsons


if __name__ == '__main__':
    pass
