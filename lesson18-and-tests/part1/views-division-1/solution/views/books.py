from flask_restx import Resource, Namespace

book_ns = Namespace('books')


@book_ns.route('/')
class BooksView(Resource):
    def get(self):
        return [], 200

    def post(self):
        return "", 201


@book_ns.route('/<int:bid>')
class BooksView(Resource):
    def get(self, bid):
        return bid, 200