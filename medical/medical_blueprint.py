import datetime
import json

from flask import Blueprint, request

from redisInit import rs
from user.model import User
from .model import Medical, db

medical_blueprint = Blueprint('medical', __name__)


def getUid():
    token = request.headers.get('Authorization')
    if token is None:
        return None
    uid = rs.get(token)
    print(uid)
    if uid is None:
        return None
    return uid.decode()


@medical_blueprint.before_request
def before_request():
    print('before_request')
    if getUid() is None:
        return {
                   'code': 0,
                   'message': '请登录'
               }, 401


# 查询病历列表
@medical_blueprint.route('/medical/query/list/<int:patient_id>', methods=['GET'])
def query_medical_list(patient_id):
    # find all medical records of a patient and find the doctor of each medical record from user
    medical_list = Medical.query.join(User, Medical.doctor_id == User.id).add_entity(User.realName)
    medical_list = medical_list.filter(Medical.patient_id == patient_id).order_by(db.desc(Medical.time)).all()
    record_list = []
    print(patient_id, medical_list)
    for record_item in medical_list:
        info = {}
        record = record_item[0]
        if record.hasInfo == 1:
            info = {
                'isFirst': record.is_First,
                'doctor_id': record.doctor_id,
                'doctor': record_item.realName,
                'now': record.now,
                'allergic': record.allergic,
                'check': json.loads(record.check_json),
                'main': record.main,
                'cure': record.cure,
                'advice': record.advice,
                'epidemic': record.epidemic,
                'history': record.history,
            }
        record_list.append({
            'id': record.id,
            'has_info': True if record.hasInfo == 1 else False,
            'info': info,
            'time': datetime.datetime.strptime(str(record.time), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
        })
    print(record_list)
    return {
        'code': 1,
        'message': '查询成功',
        'data': record_list
    }


# 添加病例列表
@medical_blueprint.route('/medical/command/add/<int:patient_id>', methods=['GET'])
def addNewEmptyRecord(patient_id):
    is_all_finish = Medical.query.filter_by(hasInfo=0, patient_id=patient_id).first()
    if is_all_finish is not None:
        print('存在未完成填写的病例记录', is_all_finish)
        return {
            'code': 0,
            'message': '请先完成已有病历信息'
        }
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_medical = Medical(patient_id=patient_id, hasInfo=0, time=now_time, doctor_id=1)
    try:
        db.session.add(new_medical)
        db.session.commit()
        return {
            'code': 1,
            'message': '添加成功'
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'message': '添加失败',
            'error': str(e)
        }


# 编辑病例列表
@medical_blueprint.route('/medical/command/edit', methods=['POST'])
def editRecord():
    record_id = request.json.get('id')
    query_record = Medical.query.filter_by(id=record_id).first()
    if query_record is None:
        return {
            'code': 0,
            'message': '病例不存在'
        }
    check = request.json.get('check')
    main = request.json.get('main')
    cure = request.json.get('cure')
    advice = request.json.get('advice')
    epidemic = request.json.get('epidemic')
    now = request.json.get('now')
    allergic = request.json.get('allergic')
    is_first = request.json.get('isFirst')
    doctor_id = request.json.get('doctor')
    history = request.json.get('history')

    query_record.check_json = json.dumps(check, ensure_ascii=False)
    query_record.main = main
    query_record.cure = cure
    query_record.advice = advice
    query_record.epidemic = epidemic
    query_record.now = now
    query_record.allergic = allergic
    query_record.is_First = is_first
    query_record.doctor_id = doctor_id
    query_record.hasInfo = 1
    query_record.history = history
    db.session.add(query_record)
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
