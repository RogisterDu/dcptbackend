import pinyin
from flask import Blueprint, request
from sqlalchemy import text, or_

from user.model import User
from .model import Charge, db

charge_blueprint = Blueprint('charge', __name__)


def getUid():
    uid = request.headers.get('Authorization')
    query_user = User.query.filter_by(id=uid).first()
    if query_user is None:
        return None
    return query_user.id


@charge_blueprint.before_request
def before_request():
    print('before_request')
    if getUid() is None:
        return {
                   'code': 0,
                   'message': '请登录'
               }, 401


@charge_blueprint.route('/charge/item/enable/query/paging', methods=['POST'])
def getChargeItem():
    name = request.json.get('name')
    pageno = int(request.json.get('pageNo'))
    pagesize = int(request.json.get('pageSize'))
    paginate_obj = Charge.query.filter(
        Charge.is_deleted == 0,
        Charge.status == 0,
        or_(Charge.name.like('%' + name + '%'),
            Charge.abbreviation.like(('%' + name + '%'))) if name is not None else text(''),
    ).paginate(pageno, pagesize, error_out=False)
    total = paginate_obj.total
    charge_list = []
    for temp in paginate_obj.items:
        charge_list.append(
            {
                'id': temp.id,
                'chargeItem': temp.name,
                'unit': temp.unit,
                'unitPrice': temp.unit_price,
                'code': temp.code,
            }
        )
    if charge_list is not None:
        print(charge_list)
        return {
            'code': 1,
            'success': True,
            'data': {
                'data': charge_list,
                'total': total
            }
        }
    else:
        return {
            'code': 0,
            'success': False,
            'message': '记录为空'
        }


@charge_blueprint.route('/charge/item/all/query/paging', methods=['POST'])
def getAllChargeItem():
    name = request.json.get('name')
    pageno = int(request.json.get('pageNo'))
    pagesize = int(request.json.get('pageSize'))
    paginate_obj = Charge.query.filter(
        Charge.is_deleted == 0,
        or_(Charge.name.like('%' + name + '%'),
            Charge.abbreviation.like(('%' + name + '%'))) if name is not None else text(''),
    ).paginate(pageno, pagesize, error_out=False)
    total = paginate_obj.total
    charge_list = []
    for temp in paginate_obj.items:
        charge_list.append(
            {
                'id': temp.id,
                'chargeItem': temp.name,
                'unit': temp.unit,
                'unitPrice': temp.unit_price,
                'code': temp.code,
                'status': temp.status,
                'type': temp.item_type,
            }
        )
    if charge_list is not None:
        print(charge_list)
        return {
            'code': 1,
            'success': True,
            'data': {
                'data': charge_list,
                'total': total
            }
        }
    else:
        return {
            'code': 0,
            'success': False,
            'message': '记录为空'
        }


@charge_blueprint.route('/charge/item/command/add', methods=['POST'])
def addNewChargeItem():
    name = request.json.get('name')
    # abbreviation = request.json.get('abbreviation')
    unit = request.json.get('unit')
    unit_price = request.json.get('unitPrice')
    status = request.json.get('status')
    code = request.json.get('code')
    item_type = request.json.get('type')

    query_charge = Charge.query.filter(
        Charge.is_deleted == 0,
        Charge.code == code,
    ).first()
    if query_charge is not None:
        return {
            'code': 0,
            'success': False,
            'message': '该编码已存在'
        }

    new_charge = Charge(
        name=name,
        abbreviation=pinyin.get_initial(name, delimiter="").upper(),
        unit=unit,
        unit_price=unit_price,
        code=code,
        status=status,
        is_deleted=0,
        item_type=item_type
    )
    try:
        db.session.add(new_charge)
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


@charge_blueprint.route('/charge/item/command/edit', methods=['POST'])
def editChargeItem():
    edit_id = request.json.get('id')
    name = request.json.get('name')
    unit = request.json.get('unit')
    unit_price = request.json.get('unitPrice')
    status = request.json.get('status')
    code = request.json.get('code')
    item_type = request.json.get('type')

    # query_charge = Charge.query.filter(
    #     Charge.is_deleted == 0,
    #     Charge.code == code,
    # ).first()
    # if query_charge is not None:
    #     return {
    #         'code': 0,
    #         'success': False,
    #         'message': '该编码已存在'
    #     }

    edit_charge = Charge.query.filter(
        Charge.id == edit_id,
    ).first()
    if edit_charge is None:
        return {
            'code': 0,
            'success': False,
            'message': '该记录不存在'
        }
    edit_charge.name = name,
    edit_charge.abbreviation = pinyin.get_initial(name, delimiter="").upper(),
    edit_charge.unit = unit,
    edit_charge.unit_price = unit_price,
    edit_charge.code = code,
    edit_charge.status = status,
    edit_charge.item_type = item_type

    db.session.add(edit_charge)
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
