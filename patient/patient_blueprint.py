import datetime
import json
import time

from flask import Blueprint, request
from sqlalchemy import or_, text, and_

from fee.model import Fee
from redisInit import rs
from .model import Patient
from .model import db

patient_blueprint = Blueprint('patient', __name__)


def getUid():
    token = request.headers.get('Authorization')
    if token is None:
        return None
    uid = rs.get(token)
    print(uid)
    if uid is None:
        return None
    return uid.decode()


@patient_blueprint.before_request
def before_request():
    print('before_request')
    if getUid() is None:
        return {
                   'code': 0,
                   'message': '请登录'
               }, 401


@patient_blueprint.route('/patient/list/paging', methods=['GET'])
def patientList():
    length = request.args.get('length', 10, type=int)
    offset = request.args.get('start', 0, type=int)
    paginate_obj = Patient.query.order_by(db.desc(Patient.last_visit)).offset(offset).limit(length).all()
    total = Patient.query.count()
    patient_list = []
    for info in paginate_obj:
        debt_fee = Fee.query.filter(and_(Fee.patient_id == info.id, Fee.should > Fee.paid)).first()
        tags = []
        if debt_fee is not None:
            tags.append('欠费')
        tags.extend(json.loads(info.tags))
        patient_list.append({
            'id': info.id,
            'name': info.name,
            'contact': info.contact,
            'tags': tags,
        })
    return {
        'code': 200,
        'msg': 'success',
        'data': {
            'total': total,
            'data': patient_list,
        }
    }


@patient_blueprint.route('/patient/command/add', methods=['POST'])
def addPatient():
    print('add a patient')
    name = request.json.get('name')
    sex = request.json.get('sex')
    contact = request.json.get('contact')
    address = request.json.get('address')
    identity_id = request.json.get('identity_id')
    history = request.json.get('history')
    allergic = request.json.get('allergic')
    habit = request.json.get('habit')
    email = request.json.get('email')
    qq = request.json.get('qq')
    tags = request.json.get('tags')

    # get now time
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    pcr = request.json.get('PCR')

    # find if the patient is existed
    patient = Patient.query.filter_by(identityID=identity_id).first()
    if patient is not None:
        patient.last_visit = now_time
        db.session.add(patient)
        db.session.commit()
        return {
            'code': 1,
            'message': '病人已存在',
            'data': {
                'id': patient.id
            }
        }
    new_patient = Patient(
        name=name,
        contact=contact,
        sex=sex,
        birthday="{0}-{1}-{2}".format(identity_id[6:10], identity_id[10:12], identity_id[12:14]),
        identityID=identity_id,
        address=address,
        last_visit=now_time,
        provinceDesc=pcr[0],
        cityDesc=pcr[1],
        disctrictDesc=len(pcr) > 2 and pcr[2] or '',
        pcr_json=json.dumps(pcr, ensure_ascii=False),
        # get birthday from identity_id
        debt=0,
        is_deleted=0,
        tags=json.dumps(tags, ensure_ascii=False) if tags is not None else '[]',
        qq=qq if qq is not None else '',
        email=email if email is not None else '',
        allergic=allergic if allergic is not None else '',
        habit=habit if habit is not None else '',
        history=history if history is not None else '',
    )
    db.session.add(new_patient)
    try:
        db.session.flush()
        new_id = new_patient.id
        db.session.commit()
        return {
            'code': 1,
            'success': True,
            'message': '添加新病人成功',
            'data': {
                'id': new_id
            }
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'success': False,
            'message': '添加失败',
            'error': str(e)
        }


@patient_blueprint.route('/patient/command/edit', methods=['POST'])
def editPatient():
    patient_id = request.json.get('id')
    query_patient = Patient.query.filter_by(id=patient_id).first()
    if query_patient is None:
        return {
            'code': 0,
            'message': '病人不存在',
        }

    name = request.json.get('name')
    sex = request.json.get('sex')
    contact = request.json.get('contact')
    address = request.json.get('address')
    identity_id = request.json.get('identity_id')
    history = request.json.get('history')
    allergic = request.json.get('allergic')
    habit = request.json.get('habit')
    email = request.json.get('email')
    qq = request.json.get('qq')
    pcr = request.json.get('PCR')
    tags = request.json.get('tags')

    query_patient.name = name
    query_patient.tags = json.dumps(tags, ensure_ascii=False) if tags is not None else '[]'
    query_patient.sex = sex
    query_patient.contact = contact
    query_patient.address = address
    query_patient.identityID = identity_id
    query_patient.history = history
    query_patient.allergic = allergic
    query_patient.habit = habit
    query_patient.qq = qq
    query_patient.email = email
    query_patient.birthday = "{0}-{1}-{2}".format(identity_id[6:10], identity_id[10:12], identity_id[12:14])
    query_patient.provinceDesc = pcr[0]
    query_patient.cityDesc = pcr[1]
    query_patient.disctrictDesc = len(pcr) > 2 and pcr[2] or ''
    query_patient.pcr_json = json.dumps(pcr, ensure_ascii=False)

    db.session.add(query_patient)
    try:
        db.session.commit()
        return {
            'code': 1,
            'message': '修改成功',
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'message': '修改失败',
        }


# get patient info by id
@patient_blueprint.route('/patient/info/<int:patient_id>', methods=['GET'])
def getPatientInfo(patient_id):
    patient = Patient.query.filter_by(id=patient_id).first()
    if patient is None:
        return {
            'code': 0,
            'message': 'patient not found',
            'data': {}
        }
    return {
        'code': 1,
        'message': 'success',
        'data': {
            'id': patient.id,
            'name': patient.name,
            'contact': patient.contact,
            'sex': patient.sex,
            'qq': patient.qq,
            'email': patient.email,
            'birth': datetime.datetime.strptime(str(patient.birthday), "%Y-%m-%d").strftime(
                "%Y-%m-%d"),
            'last_visit': datetime.datetime.strptime(str(patient.last_visit), "%Y-%m-%d").strftime(
                "%Y-%m-%d"),
            'PCR': json.loads(patient.pcr_json),
            'address': patient.address,
            'tags': json.loads(patient.tags),
            'identity_id': patient.identityID,
            'history': patient.history,
            'allergic': patient.allergic,
            'habit': patient.habit,
        }
    }


@patient_blueprint.route('/patient/list/query/fuzzy', methods=['GET'])
def fuzzyQueryPatient():
    fuzzy_query = request.args.get('fuzzy')
    if fuzzy_query is None:
        return {
            'code': 0,
            'message': 'query is empty',
            'data': {}
        }
    paginate_obj = Patient.query.filter(
        Patient.is_deleted == 0,
        or_(Patient.name.like('%' + fuzzy_query + '%'),
            Patient.contact.like('%' + fuzzy_query + '%')) if fuzzy_query is not None else text('')).order_by(
        db.desc(Patient.last_visit)).all()
    # total = Patient.query.count()
    patient_list = []
    for info in paginate_obj:
        patient_list.append({
            'id': info.id,
            'name': info.name,
            'contact': info.contact,
            # 'tags': json.loads(info.tags),
        })
    return {
        'code': 200,
        'msg': 'success',
        'data': patient_list,
    }
