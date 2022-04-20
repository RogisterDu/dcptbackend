import datetime
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

import xlwt
from flask import Blueprint, request
from sqlalchemy import and_, text

from task.model import Task
from .model import Visitor
from .model import db

visitor_blueprint = Blueprint('visitor', __name__)
executor = ThreadPoolExecutor()


# 分页查询所有访客
@visitor_blueprint.route('/visitor/query/paging', methods=['POST'])
def vistorlist():
    name = request.json.get('name')
    contact = request.json.get('contact')
    start = request.json.get('visitTimeStart')
    end = request.json.get('visitTimeEnd')

    pageno = int(request.json.get('pageNo'))
    pagesize = int(request.json.get('pageSize'))
    paginate_obj = Visitor.query.filter(
        Visitor.is_deleted == 0,
        Visitor.name.like('%' + name + '%') if name is not None else text(''),
        Visitor.contact.like('%' + contact + '%') if contact is not None else text(''),
        and_(Visitor.time >= start, Visitor.time <= end) if start is not None and end is not None else text(''),
    ).order_by(Visitor.time).paginate(pageno, pagesize, error_out=False)
    total = paginate_obj.total
    visitor_list = []
    for temp in paginate_obj.items:
        visitor_list.append(
            {
                'id': temp.id,
                'name': temp.name,
                'temperature': temp.temperature,
                'contact': temp.contact,
                # transform GMT time format to local time format
                'time': datetime.datetime.strptime(str(temp.time), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
                'pcr': json.loads(temp.pcr_json),
                'address': temp.address,
                'greenCode': temp.greenCode,
                'is_safe': temp.is_safe,
                'is_touch': temp.is_touch,
                'identityID': temp.identityID,
            }
        )
    if visitor_list is not None:
        print(visitor_list)
        return {
            'code': 1,
            'success': True,
            'data': {
                'data': visitor_list,
                'total': total
            }
        }
    else:
        return {
            'code': 0,
            'success': False,
            'message': '记录为空'
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
        provinceDesc=pcr[0],
        cityDesc=pcr[1],
        disctrictDesc=len(pcr) > 2 and pcr[2] or '',
        is_safe=is_safe,
        is_touch=is_touch,
        greenCode=green_code,
        identityID=identity_id,
        pcr_json=json.dumps(pcr, ensure_ascii=False),
        is_deleted=0
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


# 作废访客记录
@visitor_blueprint.route('/visitor/command/invalid', methods=['POST'])
def deleteVisitor():
    visitor_id = request.json.get('id')
    visitor = Visitor.query.filter(Visitor.id == visitor_id).first()
    if visitor:
        visitor.is_deleted = 1
        db.session.add(visitor)
        db.session.commit()
        return {
            'code': 1,
            'success': True,
            'message': '作废成功'
        }
    else:
        return {
            'code': 0,
            'success': False,
            'message': '作废失败'
        }


@visitor_blueprint.route('/visitor/command/export', methods=['POST'])
def exportData():
    # 新建导出任务
    # 导出状态  100 准备中 200 待下载 300 已经下载 400 失败
    new_task = Task(
        taskName='访客记录导出' + str(time.time()),
        creator_id=1,
        status=100,
        statusDesc='',
        file_url='',
    )
    db.session.add(new_task)
    # 获取新插入的任务id
    db.session.flush()
    new_task_id = new_task.id
    db.session.commit()
    print('创建准备任务成功', new_task_id)
    # Excel 异步导出
    executor.submit(exportAsExcel, new_task_id)
    return {
        'code': 1,
        'message': '已经添加进导出任务请查看导出任务列表',
    }


def exportAsExcel(task_id):
    from app import app
    with app.app_context():
        try:
            print('111', task_id)
            wb = xlwt.Workbook()
            ws = wb.add_sheet('来访日志')
            ws.write(0, 0, "名字")
            ws.write(0, 1, "联系电话")
            ws.write(0, 3, "住址")
            ws.write(0, 4, "来访时间")
            dataw = Visitor.query.all()
            print('222')
            if dataw is not None:
                for i in range(0, len(dataw)):
                    visitor_i = dataw[i]
                    ws.write(i + 1, 0, visitor_i.name)
                    ws.write(i + 1, 1, visitor_i.contact)
                    ws.write(i + 1, 2, visitor_i.address)
                    ws.write(i + 1, 3, visitor_i.time)
            now = str(time.time())
            print('222')
            path = "\\static\\excel\\"
            file_name = "visitor_" + now + ".xls"
            basedir = os.path.abspath(os.path.dirname(__file__))
            file_path = basedir + path
            # file_path = 'D:\\Project\\dcptbackend' + path
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_path = file_path + file_name
            try:
                f = open(file_path, 'r')
                f.close()
            except IOError:
                f = open(file_path, 'w')
            wb.save(file_path)
            query_task = Task.query.filter(Task.id == task_id).first()
            query_task.status = 200
            query_task.file_url = file_path
            db.session.add(query_task)
            db.session.commit()
            print('导出成功')
        except Exception as e:
            print(e)
