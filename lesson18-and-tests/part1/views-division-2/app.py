# У вас есть приложение с использованием REST X, 
# где все views, а также модель находятся в одном файле. 
# 
# Необходимо сделать рефакторинг архитектуры приложения.
# Структура приложения должна быть следующего вида:
#
# views-division-2
# ├── ./app.py       - Основной фаил, здесь инициализируется приложение
# ├── ./models.py    - В этот фаил переместите модели
# ├── ./setup_db.py  - в этом файле инициализируйте базу данных для Flask
# ├── ./test.py      - Это наши тесты, запустите после самостоятельной проверки
# └── ./views
#     └── ./views/books.py  - В этот фаил переместите class based views.
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
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

api = Api(app)
book_ns = api.namespace('books')

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)

with app.app_context():
    db.create_all()
    b1 = Book(id=1, name="Гарри Поттер и Тайная Комната",   # Формируем тестовую БД   
              author="Джоан Роулинг", year=1990)            # чтобы можно было
    b2 = Book(id=2, name="Граф Монте-Кристо",               # самостоятельно проверить 
              author="Александр Дюма", year=1844)           # работу эндпоинтов
    with db.session.begin():
        db.session.add_all([b1, b2])


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


if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
