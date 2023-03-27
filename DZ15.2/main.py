from flask import Flask
from utils import get_animal_by_id

app = Flask(__name__)


@app.route("/<itemid>", methods=["GET"])
def page_animal_by_id(itemid):
    post = get_animal_by_id(itemid)
    return post


app.run()
