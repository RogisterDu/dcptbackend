import datetime

from flask import Blueprint, request
from sqlalchemy import text

from redisInit import rs
from .model import Task, db

task_blueprint = Blueprint('task', __name__)


def getUid():
    token = request.headers.get('Authorization')
    if token is None:
        return None
    uid = rs.get(token)
    print(uid)
    if uid is None:
        return None
    return uid.decode()


@task_blueprint.before_request
def before_request():
    print('before_request')
    if getUid() is None:
        return {
                   'code': 0,
                   'message': '请登录'
               }, 401


@task_blueprint.route('/task/query/list/paging', methods=['POST'])
def queryTaskListPaging():
    page_no = request.json.get('pageNo')
    page_size = request.json.get('pageSize')
    task_status = request.json.get('taskStatus')
    paginate_obj = Task.query.filter(
        Task.status == task_status if task_status is not None else text('')
    ).order_by(db.desc(Task.finish_time)).paginate(page_no, page_size, error_out=False)
    total = paginate_obj.total
    query_dicom = paginate_obj.items
    task_list = []
    for temp in query_dicom:
        task_list.append({
            'id': temp.id,
            'taskStatus': temp.status,
            'remark': temp.statusDesc,
            'fileUrl': temp.file_url,
            'taskName': temp.taskName,
            'finishTime': datetime.datetime.strptime(str(temp.finish_time), "%Y-%m-%d %H:%M:%S").strftime(
                "%Y-%m-%d %H:%M:%S") if temp.finish_time is not None else '',
        })
    return {
        'code': 1,
        'data': {
            'data': task_list,
            'total': total
        },
        'message': '查询成功',
    }


@task_blueprint.route('/task/command/update/status', methods=['GET'])
def updateTaskStatus():
    task_id = request.args.get('taskId')
    task = Task.query.filter_by(id=task_id).first()
    task.status = 300
    task.statusDesc = '已完成'
    db.session.add(task)
    db.session.commit()
    return {
        'code': 1,
        'message': '更新成功',
    }
