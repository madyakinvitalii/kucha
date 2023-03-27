from flask import Flask
from flask_restx import Api

from models import Book, Author
from setup_db import db
from views.books import book_ns
from views.authors import author_ns


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(book_ns)
    api.add_namespace(author_ns)
    create_data(app, db)


def create_data(app, db):
    with app.app_context():
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


app = create_app()
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)






