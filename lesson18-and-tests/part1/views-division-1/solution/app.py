from flask import Flask
from flask_restx import Api

from views.books import book_ns

app = Flask(__name__)
app.url_map.strict_slashes = False

api = Api(app)

api.add_namespace(book_ns)

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)


