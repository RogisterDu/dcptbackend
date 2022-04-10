import datetime

from flask import Blueprint
from sqlalchemy import null

from user.model import User
from .model import Medical

medical_blueprint = Blueprint('medical', __name__)


@medical_blueprint.route('/medical/query/list/<int:patient_id>', methods=['GET'])
def query_medical_list(patient_id):
    # find all medical records of a patient and find the doctor of each medical record from user
    medical_list = Medical.query.join(User, Medical.doctor_id == User.id).add_entity(User.realName)
    medical_list = medical_list.filter(Medical.patient_id == patient_id).all()
    record_list = []
    for record_item in medical_list:
        info = {}
        print('111', record_item)
        record = record_item[0]
        if record.hasInfo == 1:
            info = {
                'is_First': record.is_First,
                'doctor_id': record.doctor_id,
                'doctor': record_item.realName,
                'now': record.now,
                'allergic': record.allergic,
                'check_json': record.check_json,
                'main': record.main,
                'cure': record.cure,
                'advice': record.advice,
                'epidemic': record.epidemic,
            }
        record_list.append({
            'id': record.id,
            'has_info': 'true' if record.hasInfo == 1 else 'false',
            'info': info if info else null,
            'time': datetime.datetime.strptime(str(record.time), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
        })
        return {
            'code': 1,
            'data': record_list
        }
