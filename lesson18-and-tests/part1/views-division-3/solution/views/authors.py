from flask import request
from flask_restx import Resource, Namespace
from models import Author
from setup_db import db

author_ns = Namespace('authors')

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