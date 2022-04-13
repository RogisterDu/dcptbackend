import time

from flask import Blueprint, request
from sqlalchemy import text

from .model import User, db

account_blueprint = Blueprint('account', __name__)


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


@account_blueprint.route('/account/item/command/add', methods=['POST'])
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

# @account_blueprint.route('/account/item/command/edit', methods=['POST'])
# def editaccountItem():
#     edit_id = request.json.get('id')
#     name = request.json.get('name')
#     unit = request.json.get('unit')
#     unit_price = request.json.get('unitPrice')
#     status = request.json.get('status')
#     code = request.json.get('code')
#     item_type = request.json.get('type')
#
#     # query_account = account.query.filter(
#     #     account.is_deleted == 0,
#     #     account.code == code,
#     # ).first()
#     # if query_account is not None:
#     #     return {
#     #         'code': 0,
#     #         'success': False,
#     #         'message': '该编码已存在'
#     #     }
#
#     edit_account = account.query.filter(
#         account.id == edit_id,
#     ).first()
#     if edit_account is None:
#         return {
#             'code': 0,
#             'success': False,
#             'message': '该记录不存在'
#         }
#     edit_account.name = name,
#     edit_account.abbreviation = pinyin.get_initial(name, delimiter="").upper(),
#     edit_account.unit = unit,
#     edit_account.unit_price = unit_price,
#     edit_account.code = code,
#     edit_account.status = status,
#     edit_account.item_type = item_type
#
#     db.session.add(edit_account)
#     try:
#         db.session.commit()
#         return {
#             'code': 1,
#             'success': True,
#             'message': '修改成功'
#         }
#     except Exception as e:
#         print(e)
#         return {
#             'code': 0,
#             'success': False,
#             'message': '修改失败',
#             'error': str(e)
#         }
