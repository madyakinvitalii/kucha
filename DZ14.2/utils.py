import sqlite3
import json
from flask import jsonify

# Структура таблицы
# -----------------------
# show_id — id тайтла
# type — фильм или сериал
# title — название
# director — режиссер
# cast — основные актеры
# country — страна производства
# date_added — когда добавлен на Нетфликс
# release_year — когда выпущен в прокат
# rating — возрастной рейтинг
# duration — длительность
# duration_type — минуты или сезоны
# listed_in — список жанров и подборок
# description — краткое описание


def search_by_name(name):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                            SELECT title, country, release_year, listed_in, description
                            FROM netflix
                            WHERE title LIKE '%{name}%'
                            ORDER BY 'release_year'
                            LIMIT 1
                            """

        cursor.execute(sqlite_query)
        sql_result = cursor.fetchall()
        for row in sql_result:
            result = {"title": f"{row[0]}", "country": f"{row[1]}", "release_year": f"{row[2]}", "genre": f"{row[3]}", "description": f"{row[4].strip()}"}
        json_result = json.dumps(result)
        return json_result


def search_by_range_years(first_year, second_year):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                            SELECT title, release_year
                            FROM netflix
                            WHERE release_year > '{first_year}'
                            AND release_year < '{second_year}'
                            ORDER BY 'release_year'
                            LIMIT 100
                            """

        cursor.execute(sqlite_query)
        sql_result = cursor.fetchall()
        result = []
        for row in sql_result:
            result.append({"title": f"{row[0]}", "release_year": f"{row[1]}"})
        json_result = json.dumps(result)
        return json_result


def search_by_rating_groups(group):
    rating_list = ''
    if group.lower() == 'children':
        rating_list = "('G')"
    elif group.lower() == 'family':
        rating_list = ('G', 'PG', 'PG-13')
    elif group.lower() == 'adult':
        rating_list = ('R', 'NC-17')
    else:
        return "Такой группы не существует"

    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                            SELECT title, rating, description
                            FROM netflix
                            WHERE rating IN {rating_list}
                            """
        cursor.execute(sqlite_query)
        sql_result = cursor.fetchall()
        result = []
        for row in sql_result:
            result.append({"title": f"{row[0].strip()}", "rating": f"{row[1].strip()}", "description": f"{row[2].strip()}"})
        json_result = json.dumps(result)
        return json_result


def search_by_genre(genre):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                            SELECT title, description
                            FROM netflix
                            WHERE listed_in LIKE '%{genre}%'
                            ORDER BY 'release_year' DESC
                            LIMIT 10
                            """

        cursor.execute(sqlite_query)
        sql_result = cursor.fetchall()
        result = []
        for row in sql_result:
            result.append({"title": f"{row[0].strip()}", "description": f"{row[1].strip()}"})
        json_result = json.dumps(result)
        return json_result


def step_five(actor_1, actor_2):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                            SELECT "cast", COUNT(*)
                            FROM netflix 
                            WHERE "cast" LIKE '%{actor_1}%'
                            AND "cast" LIKE '%{actor_2}%'
                            HAVING COUNT(*) >= 2
                            """
        cursor.execute(sqlite_query)
        result = cursor.fetchall()
        return result


def search_by_type_year_genre(show_type, year, genre):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sqlite_query = f"""
                            SELECT title, description
                            FROM netflix
                            WHERE "type" LIKE '%{show_type}%' 
                            AND release_year = '{year}' 
                            AND listed_in LIKE '%{genre}%'
                            ORDER BY 'release_year' DESC
                            LIMIT 10
                            """

        cursor.execute(sqlite_query)
        sql_result = cursor.fetchall()
        result = []
        for row in sql_result:
            result.append({"title": f"{row[0].strip()}", "description": f"{row[1].strip()}"})
        json_result = json.dumps(result)
        return json_result


def search_film_by_year(from_year, to_year):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        sql = "SELECT `show_id`,`title`,`type`,`release_year` from netflix where `release_year` between ? and ?"
        result = cursor.execute(sql, (from_year, to_year,))
        result = [dict(row) for row in result]
    return jsonify(result)

#print(search_by_rating_groups('children'))
print(search_film_by_year(1990, 2010))
