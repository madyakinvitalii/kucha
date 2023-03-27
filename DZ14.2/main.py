from utils import search_by_name, search_by_range_years, search_by_rating_groups, search_by_genre
from flask import Flask


app = Flask(__name__)


@app.route('/movie/<name>', methods=["GET"])
def page_by_id(name):
    film = search_by_name(name)
    return film


@app.route('/movie/<first_year>/to/<second_year>', methods=["GET"])
def page_by_range_years(first_year, second_year):
    film = search_by_range_years(first_year, second_year)
    return film


@app.route('/rating/<group>', methods=["GET"])
def page_by_groups(group):
    films = search_by_rating_groups(group)
    return films


@app.route('/genre/<genre>', methods=["GET"])
def page_by_genre(genre):
    films = search_by_genre(genre)
    return films


app.run()
