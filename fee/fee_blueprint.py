import datetime

from flask import Blueprint, request

from user.model import User
from .model import Fee, db, FeeDetail

fee_blueprint = Blueprint('fee', __name__)


# status 0 空收费项 1未收费 2欠费 3完成 4作废订单

def getUid():
    uid = request.headers.get('Authorization')
    query_user = User.query.filter_by(id=uid).first()
    if query_user is None:
        return None
    return query_user.id


@fee_blueprint.before_request
def before_request():
    print('before_request')
    if getUid() is None:
        return {
                   'code': 0,
                   'message': '请登录'
               }, 401


# 查询病人的收费信息
@fee_blueprint.route('/fee/query/list/id/<int:patient_id>', methods=['GET'])
def getPatientFee(patient_id):
    # patient_id = request.args.get('patient_id')
    all_list = Fee.query.filter_by(patient_id=patient_id, is_deleted=0).order_by(db.desc(Fee.time)).all()
    return_data = []
    if all_list is None:
        return {
            'code': 1,
            'message': '该用户暂无收费记录',
            'data': []
        }
    for item in all_list:
        charge_detail = []
        if item.status != 0:
            details = FeeDetail.query.filter_by(fee_id=item.id).all()
            if details is not None:
                for detail in details:
                    charge_detail.append({
                        'serial': detail.id,
                        'chargeItem': detail.charge_item,
                        'unitPrice': detail.unit_price,
                        'code': detail.code,
                        'quantity': detail.quantity,
                        'unit': detail.unit,
                    })
        return_data.append({
            'id': item.id,
            'time': datetime.datetime.strptime(str(item.time), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
            'chargeDetail': charge_detail,
            'paid': item.paid,
            'status': item.status,
            'shouldPay': item.should,
        })
    return {
        'code': 1,
        'data': return_data,
        'message': 'success'
    }


# 新增空收费记录
@fee_blueprint.route('/fee/command/add/id/<int:patient_id>', methods=['GET'])
def addNewEmptyFee(patient_id):
    has_empty = Fee.query.filter_by(patient_id=patient_id, status=0, is_deleted=0).first()
    if has_empty is not None:
        return {
            'code': 0,
            'message': '已存在未填写的收费记录',
        }
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_fee = Fee(patient_id=patient_id, status=0, should=0, paid=0, is_deleted=0, time=now_time)
    try:
        db.session.add(new_fee)
        db.session.commit()
        return {
            'code': 1,
            'message': 'success',
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'message': '添加失败',
            'error': str(e)
        }


# 保存收费项目
@fee_blueprint.route('/fee/command/save', methods=['POST'])
def saveFee():
    fee_id = request.json.get('fee_id')
    charge_detail = request.json.get('chargeDetail')
    fee = Fee.query.filter_by(id=fee_id, is_deleted=0).first()
    if fee is None:
        return {
            'code': 0,
            'message': '收费记录不存在',
        }
    if fee.status != 0 and fee.status != 1:
        return {
            'code': 0,
            'message': '收费记录状态不正确',
        }
    if charge_detail is None:
        return {
            'code': 0,
            'message': '收费项目不能为空',
        }
    fee_detail = FeeDetail.query.filter_by(fee_id=fee_id).all()
    try:
        if fee_detail is not None:
            for item in fee_detail:
                db.session.delete(item)
        for item in charge_detail:
            new_detail = FeeDetail(fee_id=fee_id, charge_item=item['chargeItem'], unit_price=item['unitPrice'],
                                   code=item['code'], quantity=item['quantity'], unit=item['unit'])
            db.session.add(new_detail)
        fee.status = 1
        db.session.add(fee)
        db.session.commit()
        return {
            'code': 1,
            'message': 'success',
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'message': '保存失败',
            'error': str(e)
        }


# 收费
@fee_blueprint.route('/fee/command/pay', methods=['POST'])
def toCharge():
    fee_id = request.json.get('fee_id')
    # should_pay = request.json.get('should')
    total_pay = request.json.get('total')
    new_pay = float(str(request.json.get('newPay')))
    fee = Fee.query.filter_by(id=fee_id, is_deleted=0).first()
    # Fee收费异常处理
    if fee is None:
        return {
            'code': 0,
            'message': '收费记录不存在',
        }
    if fee.status != 1 and fee.status != 2:
        return {
            'code': 0,
            'message': '收费记录状态不正确',
        }
    # FeeDetail 收费
    fee.paid = fee.paid + new_pay
    if fee.status == 1 or fee.status == 0:
        fee.should = total_pay
    if fee.paid > fee.should:
        return {
            'code': 0,
            'message': '收费金额不能大于应收金额',
        }
    if fee.paid == fee.should:
        fee.status = 3
    else:
        fee.status = 2
    try:
        db.session.add(fee)
        db.session.commit()
        return {
            'code': 1,
            'message': 'success',
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'message': '收费失败',
            'error': str(e)
        }


# 作废
@fee_blueprint.route('/fee/command/invalid/id/<int:fee_id>', methods=['GET'])
def toVoidRecord(fee_id):
    fee = Fee.query.filter_by(id=fee_id, is_deleted=0).first()
    if fee is None:
        return {
            'code': 0,
            'message': '收费记录不存在',
        }
    if fee.status == 4:
        return {
            'code': 0,
            'message': '收费记录状态不正确',
        }
    fee.status = 4
    try:
        db.session.add(fee)
        db.session.commit()
        return {
            'code': 1,
            'message': 'success',
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'message': '作废失败',
            'error': str(e)
        }
