# В этом задании Вам предстоит провести рефакторинг 
# приложения, которое работает с данными
# размещенными на https://jsonkeeper.com/ 
# 
# Задание делится на 4 шага:
#
#
# Шаг 1.
# Сохраните на сайте https://jsonkeeper.com/
# следующий json:
#
# [
#   {
#     "name": "iphone 11",
#     "brand": "apple",
#     "price": 40000
#   },
#   {
#     "name": "iphone 10",
#     "brand": "apple",
#     "price": 300000
#   },
#   {
#     "name": "redmi 9A",
#     "brand": "redmi",
#     "price": 30000
#   }
# ]
#
#
# Шаг 2.
#
# Создайте файл config.py, в котором создайте класс 'Config':
#
# - Сохраните в аттрибуте API_URL созданного класса 'Config'
#   ссылку на хранилище, которую вы получили на сайте https://jsonkeeper.com/
# - В аттрибуте SQLALCHEMY_DATABASE_URI сохраните путь к базе данных.
# - Аттрибуту SQLALCHEMY_TRACK_MODIFICATIONS присвойте значение False,
#   в соответствии с текущими настройками.
#
#   
# Шаг 3.
#
# Запустите приложение и сделайте GET-запрос на адрес http://127.0.0.1/import,
# который добавит объекты с сайта хранилища в базу данных,
# используя модель Phone и сериализатор к ней.
# Обратите внимание, этот эндпоинт учебный и не соответствует правилам REST. 
# Пожалуйста, не создавайте такие эндпоинты в боевых проектах.
#
#
# Шаг 4.
#
# Cделайте GET-запрос на адрес http://127.0.0.1/phones, который
# вернет ответ со списком ранее загруженных в базу телефонов


import requests
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # TODO cохраните данные настройки 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False         # в классе Сonfig файла config.py
db = SQLAlchemy(app)


class Phone(db.Model):
    __tablename__ = 'phone'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    price = db.Column(db.Integer)


db.create_all()


@app.route("/import")
def import_data():
    data = requests.get(url='https://jsonkeeper.com/b/QBYO') # TODO Здесь добавьте ссылку на внешнее хранилище
    for d in data.json():
        p = Phone(**d)
        with db.session.begin():
            db.session.add(p)
    return "", 200


@app.route("/phones")
def phones():
    phones_data = Phone.query.all()
    res = []
    for s in phones_data:
        sm_d = s.__dict__ 
        del sm_d['_sa_instance_state']
        res.append(sm_d)
    return jsonify(res), 200


if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
