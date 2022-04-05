from flask import Flask
from config import Config
from database import db
from auth import auth_blueprint

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(auth_blueprint)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
