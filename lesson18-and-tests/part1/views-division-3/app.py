# У вас есть приложение с использованием REST X, 
# где все views, а также модель находятся в одном файле. 
# 
# Необходимо сделать рефакторинг архитектуры приложения.
# Структура приложения должна быть следующего вида:
#
# views-division-3
# ├── ./app.py       - Основной фаил, здесь инициализируется приложение
# ├── ./models.py    - В этот фаил переместите модели
# ├── ./setup_db.py  - в этом файле инициализируйте базу данных для Flask
# ├── ./test.py      - Это наши тесты, запустите после самостоятельной проверки
# └── ./views
#     ├── ./views/books.py   - В эти фаилы переместите необходимые
#     └── ./views/authors.py   для работы class based views.
# 
# Требования к выполнению задания:
# - Приложение должно соответствовать структуре выше.
# - В файле app.py не должно быть лишних переменных.
# - Приложение должно запускаться.
# - Запрос на эндпоинт должен возвращать корректный код.
#
# Менять значения, возвращаемые view-функциями, 
# а также url-адреаса в данном задании не требуется.
# Также задание содержит упрощенный вариант сериализации/десериализации
# которым мы пользуемся только в учебных целях для сокращения объема кода.

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
book_ns = api.namespace('books')
author_ns = api.namespace('authors')

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)

db.create_all()
a1 = Author(id=1, name="Джоан Роулинг", age=1965)          # Формируем тестовую базу данных
a2 = Author(id=2, name="Александр Дюма", age=1802)         # для того чтобы можно было 
b1 = Book(id=1, name="Гарри Поттер и Тайная Комната",      # самостоятельно проверить 
          author="Джоан Роулинг", year=1990)               # работу эндпоинтов
b2 = Book(id=2, name="Граф Монте-Кристо", 
          author="Александр Дюма", year=1844)
b3 = Book(id=3, name="Гарри Поттер и Орден Феникса", 
          author="Джоан Роулинг", year=1993)
with db.session.begin():
    db.session.add_all([b1, b2, b3, a1, a2])


@book_ns.route('/')
class BooksView(Resource):
    def get(self):                            
        books = Book.query.all()
        res = []
        for book in books:                    
            sm_d = book.__dict__              
            del sm_d['_sa_instance_state']    
            res.append(book.__dict__)
        return res, 200

    def post(self):
        data = request.json
        new_book = Book(name=data.get('name'),
                        author=data.get('author'),
                        year=data.get('year'))
        with db.session.begin():
            db.session.add(new_book)
        return "", 201


@book_ns.route('/<int:bid>')
class BookView(Resource):
    def get(self, bid):
        book = Book.query.get(bid)
        result = book.__dict__
        del result['_sa_instance_state']
        return result, 200


@author_ns.route('/')
class AuthorsView(Resource):
    def get(self):
        authors = Author.query.all()
        result = []
        for s in authors:
            instance = s.__dict__
            del instance['_sa_instance_state']
            result.append(instance)
        return result, 200

    def post(self):
        data = request.json
        new_author = Author(name=data.get('name'),
                            age=data.get('age'))
        with db.session.begin():
            db.session.add(new_author)
        return "", 201


@author_ns.route('/<int:aid>')
class AuthorView(Resource):
    def get(self, aid):
        author = Author.query.get_or_404(aid)
        res = author.__dict__
        del res['_sa_instance_state']
        return res, 200


if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
