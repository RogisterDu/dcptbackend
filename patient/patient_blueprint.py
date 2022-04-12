import datetime
import json
import time

from flask import Blueprint, request
from sqlalchemy import or_, text

from .model import Patient
from .model import db

patient_blueprint = Blueprint('patient', __name__)


@patient_blueprint.route('/patient/list/paging', methods=['GET'])
def patientList():
    length = request.args.get('length', 10, type=int)
    offset = request.args.get('start', 0, type=int)
    paginate_obj = Patient.query.order_by(db.desc(Patient.last_visit)).offset(offset).limit(length).all()
    total = Patient.query.count()
    patient_list = []
    for info in paginate_obj:
        patient_list.append({
            'id': info.id,
            'name': info.name,
            'contact': info.contact,
            'tags': json.loads(info.tags),
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
    # get now time
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    pcr = request.json.get('PCR')

    # find if the patient is existed
    patient = Patient.query.filter_by(identityID=identity_id).first()
    if patient is not None:
        return {
            'code': 1,
            'message': 'patient is exist',
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
        tags='[]',
    )
    db.session.add(new_patient)
    try:
        new_id = db.session.flush()
        db.session.commit()
        return {
            'code': 1,
            'success': True,
            'message': '添加成功',
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
            'last_visit': patient.last_visit,
            'pcr': json.loads(patient.pcr_json),
            'address': patient.address,
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
