import datetime
import time

from flask import Blueprint, request
from sqlalchemy import text

from .model import Task, db

task_blueprint = Blueprint('task', __name__)


@task_blueprint.route('/task/query/list/paging', methods=['POST'])
def queryTaskListPaging():
    page_no = request.json.get('pageNo')
    page_size = request.json.get('pageSize')
    task_status = request.json.get('taskStatus')
    paginate_obj = Task.query.filter(
        Task.status == task_status if task_status is not None else text('')
    ).paginate(page_no, page_size, error_out=False)
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
    task.finish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    db.session.add(task)
    db.session.commit()
    return {
        'code': 1,
        'message': '更新成功',
    }
