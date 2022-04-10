from flask import Flask

from config import Config
from database import db
from medical.medical_blueprint import medical_blueprint
from patient.patient_blueprint import patient_blueprint
from user.auth import auth_blueprint
from vistor.visitor_blueprint import visitor_blueprint

app = Flask(__name__)

# 注册数据库
app.config.from_object(Config)
db.init_app(app)

# 注册蓝图
app.register_blueprint(auth_blueprint)
app.register_blueprint(visitor_blueprint)
app.register_blueprint(patient_blueprint)
app.register_blueprint(medical_blueprint)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.debug = True
    app.run()
