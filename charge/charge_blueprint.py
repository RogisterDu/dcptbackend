from flask import Blueprint, request
from sqlalchemy import text, or_

from .model import Charge

charge_blueprint = Blueprint('charge', __name__)


@charge_blueprint.route('/charge/item/query/paging', methods=['POST'])
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
