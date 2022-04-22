import time

from flask import Blueprint, request
from sqlalchemy import text

from redisInit import rs
from .model import User, db

account_blueprint = Blueprint('account', __name__)


def getUid():
    token = request.headers.get('Authorization')
    uid = rs.get(token)
    print(uid)
    if uid is None:
        return None
    return uid.decode()


@account_blueprint.before_request
def before_request():
    print('before_request')
    if getUid() is None:
        return {
                   'code': 0,
                   'message': '请登录'
               }, 401


@account_blueprint.route('/account/normal/query/paging', methods=['POST'])
def getAccountList():
    name = request.json.get('name')
    pageno = int(request.json.get('pageNo'))
    pagesize = int(request.json.get('pageSize'))
    paginate_obj = User.query.filter(
        User.is_deleted == 0,
        User.name.like('%' + name + '%') if name is not None else text(''),
        User.jurisdiction == 0,
    ).paginate(pageno, pagesize, error_out=False)

    total = paginate_obj.total
    account_list = []
    for temp in paginate_obj.items:
        account_list.append(
            {
                'id': temp.id,
                'account': temp.account,
                'realName': temp.realName,
                'phone': temp.phone,
                'status': temp.status,
                'lastLogin': temp.last_login
            }
        )
    if account_list is not None:
        print(account_list)
        return {
            'code': 1,
            'success': True,
            'data': {
                'data': account_list,
                'total': total
            }
        }
    else:
        return {
            'code': 0,
            'success': False,
            'message': '记录为空'
        }


@account_blueprint.route('/account/command/add', methods=['POST'])
def addNewAccountItem():
    account = request.json.get('account')
    phone = request.json.get('phone')
    new_password = request.json.get('password')
    real_name = request.json.get('realName')
    status = request.json.get('status')

    query_account = User.query.filter(
        User.is_deleted == 0,
        User.account == account
    ).first()
    if query_account is not None:
        return {
            'code': 0,
            'success': False,
            'message': '已存在相同账号名的账号'
        }

    new_account = User(
        account=account,
        phone=phone,
        password=new_password,
        realName=real_name,
        jurisdiction=0,
        is_deleted=0,
        status=status,
        last_login=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        created_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        created_Id=1,
    )
    try:
        db.session.add(new_account)
        db.session.commit()
        return {
            'code': 1,
            'success': True,
            'message': '添加成功'
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'success': False,
            'message': '添加失败'
        }


@account_blueprint.route('/account/command/edit', methods=['POST'])
def editAccount():
    edit_id = request.json.get('id')
    account = request.json.get('account')
    phone = request.json.get('phone')
    new_password = request.json.get('password')
    real_name = request.json.get('realName')
    status = request.json.get('status')

    edit_account = User.query.filter(
        User.id == edit_id,
    ).first()
    if edit_account is None:
        return {
            'code': 0,
            'success': False,
            'message': '该记录不存在'
        }
    edit_account.account = account,
    edit_account.phone = phone,
    edit_account.password = new_password if new_password is not None else edit_account.password,
    edit_account.realName = real_name,
    edit_account.status = status,

    db.session.add(edit_account)
    try:
        db.session.commit()
        return {
            'code': 1,
            'success': True,
            'message': '修改成功'
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'success': False,
            'message': '修改失败',
            'error': str(e)
        }


@account_blueprint.route('/doctor/query/list', methods=['GET'])
def getDoctorList():
    doctor = User.query.all()
    doctor_list = []
    for i in doctor:
        doctor_list.append({
            'code': i.id,
            'desc': i.realName,
        })
    return {
        'code': 1,
        'data': {
            'data': doctor_list
        }
    }


@account_blueprint.route('/account/access', methods=['GET'])
def getAccess():
    user_id = getUid()
    query_user = User.query.filter_by(id=user_id).first()
    if query_user is None:
        return {
            'access': False,
            'message': '该用户不存在'
        }
    if query_user.jurisdiction == 0:
        return {
            'access': False,
            'message': '没有权限'
        }
    return {
        'access': True,
        'message': '欢迎访问'
    }


@account_blueprint.route('/account/command/self/edit', methods=['POST'])
def editSelfAccount():
    real_name = request.json.get('realName')
    phone = request.json.get('phone')
    uid = getUid()
    edit_account = User.query.filter(
        User.id == uid,
    ).first()
    if edit_account is None:
        return {
            'code': 0,
            'message': '账号不存在'
        }
    if edit_account.status == 0:
        return {
            'code': 0,
            'message': '账号已被禁用'
        }
    edit_account.realName = real_name
    edit_account.phone = phone
    db.session.add(edit_account)
    try:
        db.session.commit()
        return {
            'code': 1,
            'message': '修改成功'
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'message': '修改失败',
            'error': str(e)
        }


@account_blueprint.route('/account/command/self/info', methods=['GET'])
def getSelfAccountInfo():
    uid = getUid()
    query_user = User.query.filter_by(id=uid).first()
    if query_user is None:
        return {
            'code': 0,
            'message': '账号不存在'
        }
    if query_user.status == 0:
        return {
            'code': 0,
            'message': '账号已被禁用'
        }
    return {
        'code': 1,
        'data': {
            'realName': query_user.realName,
            'phone': query_user.phone,
        }
    }
