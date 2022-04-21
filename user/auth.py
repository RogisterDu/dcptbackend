from flask import Blueprint, request

from .model import User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(account=username, password=password).first()
    if user is not None:
        return {
            'code': 1,
            'token': user.id,
            'userInfo': {
                'id': user.id,
                'name': user.realName,
                'Avatar': 'https://joeschmoe.io/api/v1/random',
            }
        }
    else:
        return {
            'code': 0,
            'message': '用户名或者密码错误'
        }


