from flask import Flask

from charge.charge_blueprint import charge_blueprint
# class Config:
#     HOST = 'IP地址'
#     PORT = '端口'
#     DATABASE = '数据库名'
#     USERNAME = '用户名'
#     PASSWORD = '密码'
#
#     DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4"\
#         .format(username=USERNAME, password=PASSWORD, host=HOST, port=PORT, db=DATABASE)
#
#     SQLALCHEMY_DATABASE_URI = DB_URI
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ECHO = True
#
#     SCHEDULER_API_ENABLED = True
# 引入数据库配置
from config import Config
from database import db
from dicom.dicom_blueprint import dicom_blueprint
from fee.fee_blueprint import fee_blueprint
from medical.medical_blueprint import medical_blueprint
from medical.template_blueprint import template_blueprint
from patient.patient_blueprint import patient_blueprint
# 引入redis
from redisInit import rs
from reservation.reserve_blueprint import reserve_blueprint
from task.task_blueprint import task_blueprint
from user.account_blueprint import account_blueprint
from user.auth import auth_blueprint
from vistor.visitor_blueprint import visitor_blueprint

# 引入蓝图
# 引入 flask-redis

app = Flask(__name__)

# 注册数据库
app.config.from_object(Config)
db.init_app(app)
rs.init_app(app)

# 注册蓝图
app.register_blueprint(auth_blueprint)
app.register_blueprint(visitor_blueprint)
app.register_blueprint(patient_blueprint)
app.register_blueprint(medical_blueprint)
app.register_blueprint(charge_blueprint)
app.register_blueprint(fee_blueprint)
app.register_blueprint(reserve_blueprint)
app.register_blueprint(account_blueprint)
app.register_blueprint(template_blueprint)
app.register_blueprint(dicom_blueprint)
app.register_blueprint(task_blueprint)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.debug = True
    app.run()
