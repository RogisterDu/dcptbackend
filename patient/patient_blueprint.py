import json
import time

from flask import Blueprint, request

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
        patient_list.append(info.to_dict())
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
            'code': 2,
            'message': 'patient is exist',
            'data': {
                'patient_id': patient.id
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
    )
    db.session.add(new_patient)
    try:
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
            'message': '添加失败',
            'error': str(e)
        }
