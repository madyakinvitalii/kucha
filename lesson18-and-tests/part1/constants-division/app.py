# У вас есть приложение с использованием REST X, 
# где все views, а также модель находятся в одном файле. 
# 
# Необходимо сделать рефакторинг архитектуры приложения.
# Структура приложения должна быть следующего вида:
#
# constants-division
# ├── ./app.py       - Основной фаил, здесь инициализируется приложение
# ├── ./constants.py - В этот файл переместите константы
# ├── ./models.py    - В этот фаил переместите модели
# ├── ./setup_db.    - в этом файле инициализируйте базу данных для Flask
# ├── ./test.py      - Это наши тесты, запустите после самостоятельной проверки
# └── ./views
#     ├── ./views/files.py        - В эти фаилы переместите необходимые
#     └── ./views/smartphones.py    для работы class based views.
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


from flask import Flask
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

DOWN_PAYMENT = 0.2
ANNUAL_RATE = 0.3

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


class SmartPhone(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    path = db.Column(db.String(100))
    size = db.Column(db.Integer)


db.create_all()
f1 = File(id=1, name='config.cfg', path='/var/', size=500)
f2 = File(id=2, name='run.exe', path='/var/lib/', size=500)
sp1 = SmartPhone(id=1, name="iphone", price=100000)
sp2 = SmartPhone(id=2, name="android", price=110000)
with db.session.begin():
    db.session.add_all([f1, f2])
    db.session.add_all([sp1, sp2])

sm_ns = api.namespace('smartphones')


@sm_ns.route('/')
class SmartPhonesView(Resource):
    def get(self):
        sms = SmartPhone.query.all()
        res = []
        for s in sms:
            sm_d = s.__dict__
            del sm_d['_sa_instance_state']
            down_payment = sm_d["price"] * DOWN_PAYMENT
            sm_d["down_payment"] = down_payment
            sm_d["monthly_fee"] = ((sm_d["price"] - down_payment) * (1 + ANNUAL_RATE)) / 12
            res.append(sm_d)
        return res, 200


@sm_ns.route('/<int:nid>')
class SmartPhoneView(Resource):
    def get(self, nid):
        s = SmartPhone.query.get_or_404(nid)
        sm_d = s.__dict__
        del sm_d['_sa_instance_state']
        down_payment = sm_d["price"] * DOWN_PAYMENT
        sm_d["down_payment"] = down_payment
        sm_d["monthly_fee"] = ((sm_d["price"] - down_payment) * (1 + ANNUAL_RATE)) / 12
        return sm_d, 200


file_ns = api.namespace('files')


@file_ns.route('/')
class FilesView(Resource):
    def get(self):
        files = File.query.all()
        res = []
        for s in files:
            sm_d = s.__dict__
            del sm_d['_sa_instance_state']
            res.append(sm_d)
        return res, 200

    def post(self):
        return "", 201


@file_ns.route('/<int:fid>')
class FileView(Resource):
    def get(self, fid):
        file = File.query.get_or_404(fid)
        sm_d = file.__dict__
        del sm_d['_sa_instance_state']
        return sm_d, 200


if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)

