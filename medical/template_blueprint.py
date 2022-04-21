from flask import Blueprint, request

from user.model import User
from .model import Templet, db

template_blueprint = Blueprint('template', __name__)


def getUid():
    uid = request.headers.get('Authorization')
    query_user = User.query.filter_by(id=uid).first()
    if query_user is None:
        return None
    return query_user.id


@template_blueprint.before_request
def before_request():
    print('before_request')
    if getUid() is None:
        return {
                   'code': 0,
                   'message': '请登录'
               }, 401


@template_blueprint.route('/templet/query/list', methods=['GET'])
def queryTemplateList():
    templet_list = Templet.query.all()
    if templet_list is None:
        return {
            'code': 0,
            'data': [],
            'message': '不存在可用的模板'
        }
    temp_list = []
    for item in templet_list:
        temp_list.append({
            'id': item.id,
            'title': item.name,
            'allergic': item.allergic,
            'main': item.main,
            'now': item.now,
            'cure': item.cure,
            'epidemic': item.epidemic,
            'advice': item.advice,
            'history': item.history,
        })
    return {
        'code': 1,
        'data': temp_list,
        'message': '查询成功'
    }


@template_blueprint.route('/templet/command/save', methods=['POST'])
def saveAsTemplate():
    name = request.json.get('name')
    allergic = request.json.get('allergic')
    main = request.json.get('main')
    now = request.json.get('now')
    cure = request.json.get('cure')
    epidemic = request.json.get('epidemic')
    advice = request.json.get('advice')

    query_result = Templet.query.filter_by(name=name).first()
    if query_result is not None:
        return {
            'code': 0,
            'message': '该模板名称已存在'
        }
    new_templet = Templet(name=name, allergic=allergic, main=main, now=now, cure=cure, epidemic=epidemic, advice=advice)
    try:
        db.session.add(new_templet)
        db.session.commit()
        return {
            'code': 1,
            'message': '保存成功'
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'message': '保存失败',
            'error': str(e)
        }


@template_blueprint.route('/templet/command/delete', methods=['GET'])
def deleteTemplate():
    query_id = request.args.get('id')
    query_result = Templet.query.filter(Templet.id == query_id).first()
    if query_result is None:
        return {
            'code': 0,
            'message': "该病例模板不存在"
        }
    try:
        db.session.delete(query_result)
        db.session.commit()
        return {
            'code': 1,
            'message': "删除成功"
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'message': '保存失败',
            'error': str(e)
        }
