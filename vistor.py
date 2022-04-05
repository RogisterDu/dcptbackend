from flask import Blueprint, request
from model import Vistor

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/dpct/vistorlist', methods=['GET'])
def vistorlist():
    pageNo = request.args.get('pageNo')
    pageSize = request.args.get('pageSize')
    # getVistorList(pageNo, pageSize)
    paginate_obj = Vistor.query.paginate(
        page=pageNo, per_page=pageSize, error_out=True)
    total_Page = paginate_obj.pages
    vistor_list = paginate_obj.items
    if vistor_list:
        return {
            'code': 200,
            'msg': '获取成功',
            'data': {
                'total_Page': total_Page,
                'data': [vistor.to_json() for vistor in vistor_list]
            }
        }
    else:
        return {
            'code': 400,
            'msg': '获取失败',
            'data': {}
        }
