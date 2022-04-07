import json
import time

from flask import Blueprint, request
from .model import db
from .model import Visitor

visitor_blueprint = Blueprint('visitor', __name__)


# 分页查询所有访客
@visitor_blueprint.route('/visitor/query/paging', methods=['POST'])
def vistorlist():
    pageno = int(request.json.get('pageNo'))
    pagesize = int(request.json.get('pageSize'))
    paginate_obj = Visitor.query.paginate(pageno, pagesize, error_out=False)
    total_page = paginate_obj.pages
    visitor_list = []
    for temp in paginate_obj.items:
        visitor_list.append(
            {
                'id': temp.id,
                'name': temp.name,
                'temperature': temp.temperature,
                'contact': temp.contact,
                'time': temp.time,
                'address': temp.address,
            }
        )
    if visitor_list:
        print(visitor_list)
        return {
            'code': 1,
            'success': True,
            'data': {
                'data': visitor_list,
                'total': total_page
            }
        }


# 添加访客记录
@visitor_blueprint.route('/visitor/command/addVisitor', methods=['POST'])
def addVisitor():
    # print(request.get_json())
    # add a new visitor
    name = request.json.get('name')
    temperature = request.json.get('temperature')
    contact = request.json.get('contact')
    address = request.json.get('address')
    # get now time
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    pcr = request.json.get('PCR')
    is_safe = request.json.get('is_safe')
    is_touch = request.json.get('is_touch')
    identity_id = request.json.get('identityID')
    green_code = request.json.get('greenCode')
    new_visitor = Visitor(
        name=name,
        temperature=temperature,
        contact=contact,
        address=address,
        time=now_time,
        provinceId=pcr[0]['value'],
        provinceDesc=pcr[0]['label'],
        cityId=pcr[1]['value'],
        cityDesc=pcr[1]['label'],
        disctrictId=pcr[2]['value'],
        disctrictDesc=pcr[2]['label'],
        is_safe=is_safe,
        is_touch=is_touch,
        greenCode=green_code,
        identityID=identity_id,
    )
    db.session.add(new_visitor)
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
            'message': '添加失败'
        }

