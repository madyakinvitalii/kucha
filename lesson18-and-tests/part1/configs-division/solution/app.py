import requests
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from config import Config

config = Config()

app = Flask(__name__)
app.config.from_object(config)
app.url_map.strict_slashes = False
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
    data = requests.get(url=app.config.get("API_URL"))
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

