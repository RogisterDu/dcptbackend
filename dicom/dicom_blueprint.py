import datetime
import json

from flask import Blueprint, request

from user.model import User
from .model import Dicom

dicom_blueprint = Blueprint('dicom', __name__)


def getUid():
    uid = request.headers.get('Authorization')
    query_user = User.query.filter_by(id=uid).first()
    if query_user is None:
        return None
    return query_user.id


@dicom_blueprint.before_request
def before_request():
    print('before_request')
    if getUid() is None:
        return {
                   'code': 0,
                   'message': '请登录'
               }, 401


@dicom_blueprint.route('/dicom/query/list/paginate', methods=['POST'])
def query_list():
    patient_id = request.json.get('patient_id')
    page_no = request.json.get('pageNo')
    page_size = request.json.get('pageNo')
    paginate_obj = Dicom.query.filter(Dicom.patient_id == patient_id).paginate(page_no, page_size, error_out=False)
    total = paginate_obj.total
    query_dicom = paginate_obj.items
    dicom_list = []
    for temp in query_dicom:
        dicom_list.append({
            'id': temp.id,
            'url': json.loads(temp.dicom_url),
            'time': datetime.datetime.strptime(str(temp.time), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        })
    return {
        'code': 1,
        'data': {
            'data': dicom_list,
            'total': total
        },
        'message': '查询成功',
    }
