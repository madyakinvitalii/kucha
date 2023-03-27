# Имеется наполненная БД с таблицей guide и полуготовый код на фласке.
# Напишите представления для следующих ендпоинтов:
#
# Method: GET
# URL: /guides
# Response: [{guide_json}, {guide_json}, {guide_json}]
#
# Method: GET
# URL: /guides/1
# Response: { <guide_json> }
#
#
import json

from flask import Flask
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from guides_sql import CREATE_TABLE, INSERT_VALUES

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)
with db.session.begin():
    db.session.execute(text(CREATE_TABLE))
    db.session.execute(text(INSERT_VALUES))


class Guide(db.Model):
    __tablename__ = 'guide'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String)
    full_name = db.Column(db.String)
    tours_count = db.Column(db.Integer)
    bio = db.Column(db.String)
    is_pro = db.Column(db.Boolean)
    company = db.Column(db.Integer)


@app.route("/guides")
def get_guides():
    guides_list = Guide.query.all()
    guides_response = []

    for guide in guides_list:
        guides_response.append(
            {
                "id": guide.id,
                "surname": guide.surname,
                "full_name": guide.full_name,
                "tours_count": guide.tours_count,
                "bio": guide.bio,
                "is_pro": guide.is_pro,
                "company": guide.company
            }
        )

    return json.dumps(guides_response)


@app.route("/guides/<int:gid>")
def get_guide(gid):
    guide = Guide.query.get(gid)

    if guide is None:
        return "Guide not found"

    return json.dumps({
        "id": guide.id,
        "surname": guide.surname,
        "full_name": guide.full_name,
        "tours_count": guide.tours_count,
        "bio": guide.bio,
        "is_pro": guide.is_pro,
        "company": guide.company
    })

# чтобы увидеть результат работы функций
# запустите фаил и
# перейдите по адресу:
# 127.0.0.1:5000/guides
# 127.0.0.1:5000/guides/1


if __name__ == "__main__":
    app.run()
