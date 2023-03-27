# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies_schema = MovieSchema(many=True)
        all_movies = db.session.query(Movie)
        return movies_schema.dumps(all_movies, ensure_ascii=False), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)

        return "", 201


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid: int):
        try:
            movie = db.session.get(Movie, uid)
            movie_schema = MovieSchema()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return "", 404


    def put(self, uid):
        movie = db.session.query(Movie).get(uid)
        req_json = request.json

        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def delete(self, uid: int):
        movie = db.session.query(Movie).get(uid)

        db.session.delete(movie)
        db.session.commit()

        return "", 204



@movie_ns.route('/director_id=<int:uid>')
class DirectorMoviesView(Resource):
    def get(self, uid: int):
        try:
            movies_schema = MovieSchema(many=True)
            movies = db.session.query(Movie).filter(Movie.director_id == uid).all()
            return movies_schema.dumps(movies, ensure_ascii=False), 200
        except Exception as e:
            return "", 404


@movie_ns.route('/genre_id=<int:uid>')
class GenreMoviesView(Resource):
    def get(self, uid: int):
        try:
            genre_movies_schema = MovieSchema(many=True)
            genre_movies = db.session.query(Movie).filter(Movie.genre_id == uid)
            return genre_movies_schema.dumps(genre_movies, ensure_ascii=False), 200
        except Exception as e:
            return "", 404


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors_schema = DirectorSchema(many=True)
        all_directors = db.session.query(Director)
        return directors_schema.dumps(all_directors, ensure_ascii=False), 200


@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid: int):
        try:
            director = db.session.get(Director, uid)
            director_schema = DirectorSchema()
            return director_schema.dump(director), 200
        except Exception as e:
            return "", 404


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres_schema = GenreSchema(many=True)
        all_genress = db.session.query(Genre)
        return genres_schema.dumps(all_genress, ensure_ascii=False), 200


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid: int):
        try:
            genre = db.session.get(Genre, uid)
            genre_schema = GenreSchema()
            return genre_schema.dump(genre), 200
        except Exception as e:
            return "", 404


if __name__ == '__main__':
    app.run(debug=True)
