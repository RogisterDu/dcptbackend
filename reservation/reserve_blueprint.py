import calendar
import datetime

from flask import Blueprint, request
from sqlalchemy import and_, text

from patient.model import Patient
from user.model import User
from .model import Reserve, db

reserve_blueprint = Blueprint('reserve', __name__)


@reserve_blueprint.route('/reserve/command/list/time/query', methods=['POST'])
def getReservationByTime():
    start_time = request.json.get('startAt')
    end_time = request.json.get('endAt')
    # 禁止同时输入startAt endAt 和 year month
    # if start_time is not None and end_time is not None and query_year is None and query_month is not None:
    #     return {
    #         'code': 0,
    #         'message': '禁止同时输入startAt endAt 和 year month',
    #         'data': []
    #     }
    # 搜索
    day_list = Reserve.query.filter(
        and_(Reserve.reserve_time >= start_time, Reserve.reserve_time <= end_time)
        if start_time is not None and end_time is not None else text(''),
    )
    day_list = day_list.join(User, User.id == Reserve.doctor_id).join(Patient,
                                                                      Reserve.patient_id == Patient.id)
    day_list = day_list.add_entity(User).add_entity(Patient).all()
    print("查询结果", day_list)

    if day_list is None:
        return {
            'code': 0,
            'data': [],
            'message': '查询失败'
        }
    status_list = ["success", "default", "error"]
    return_result = []
    for item in day_list:
        return_result.append({
            'id': item[0].id,
            'type': status_list[item[0].rank],
            'rank': item[0].rank,
            'title': item[0].title,
            'time': datetime.datetime.strptime(str(item[0].reserve_time), "%Y-%m-%d %H:%M:%S").strftime(
                "%Y-%m-%d %H:%M:%S"),
            'doctor_Id': item[0].doctor_id,
            'doctorName': item[1].realName,
            'patientId': item[0].patient_id,
            'patientName': item[2].name,
            'description': item[0].description,
        })
    return {
        'code': 1,
        'data': return_result,
        'message': '查询成功'
    }


@reserve_blueprint.route('/reserve/command/list/date/query', methods=['POST'])
def getReservationByDate():
    query_year = request.json.get('year')
    query_month = request.json.get('month')
    query_start = None
    query_end = None
    if query_year is not None and query_month is not None:
        # 获得搜索日期的第一天和最后一天
        week_day, month_day_count = calendar.monthrange(query_year, query_month)
        query_start = datetime.datetime(query_year, query_month, 1, 0, 0, 0)
        query_end = datetime.datetime(query_year, query_month, day=month_day_count, hour=23, minute=59, second=59)

    day_list = Reserve.query.filter(
        and_(Reserve.reserve_time >= query_start, Reserve.reserve_time <= query_end)
        if query_start is not None and query_end is not None else text(''),
    )
    day_list = day_list.join(User, User.id == Reserve.doctor_id).join(Patient,
                                                                      Reserve.patient_id == Patient.id)
    day_list = day_list.add_entity(User).add_entity(Patient).all()
    print("查询结果", day_list)

    if day_list is None:
        return {
            'code': 0,
            'data': [],
            'message': '查询失败'
        }
    status_list = ["success", "default", "error"]
    return_result = []
    for item in day_list:
        return_result.append({
            'id': item[0].id,
            'type': status_list[item[0].rank],
            'rank': item[0].rank,
            'title': item[0].title,
            'time': datetime.datetime.strptime(str(item[0].reserve_time), "%Y-%m-%d %H:%M:%S").strftime(
                "%Y-%m-%d %H:%M:%S"),
            'doctor_Id': item[0].doctor_id,
            'doctorName': item[1].realName,
            'patientId': item[0].patient_id,
            'patientName': item[2].name,
            'description': item[0].description,
        })
    return {
        'code': 1,
        'data': return_result,
        'message': '查询成功'
    }


@reserve_blueprint.route('/reserve/command/add', methods=['POST'])
def addNewReservation():
    # 获取前端传来的数据
    doctor_id = request.json.get('doctorId')
    patient_id = request.json.get('patientId')
    reserve_time = request.json.get('time')
    title = request.json.get('title')
    rank = request.json.get('rank')
    description = request.json.get('description')
    # 检查数据
    if doctor_id is None or patient_id is None \
            or reserve_time is None or title is None or rank is None or description is None:
        return {
            'code': 0,
            'message': '参数错误'
        }
    # 检查医生是否存在
    doctor = User.query.filter_by(id=doctor_id).first()
    if doctor is None:
        return {
            'code': 0,
            'message': '医生不存在'
        }
    # 检查患者是否存在
    patient = Patient.query.filter_by(id=patient_id).first()
    if patient is None:
        return {
            'code': 0,
            'message': '患者不存在'
        }
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    format_pattern = '%Y-%m-%d %H:%M:%S'
    # 检查时间是否合法
    if (datetime.datetime.strptime(str(reserve_time), format_pattern) - datetime.datetime.strptime(now_time,
                                                                                                   format_pattern)).days < 0:
        return {
            'code': 0,
            'message': '时间不合法'
        }

    new_reserve = Reserve(
        doctor_id=doctor_id,
        patient_id=patient_id,
        reserve_time=reserve_time,
        title=title,
        description=description,
        rank=rank,
        operator_id=doctor_id,
    )
    db.session.add(new_reserve)
    try:
        db.session.commit()
        return {
            'code': 1,
            'message': '预约成功'
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'message': '预约失败',
            'error': str(e)
        }


@reserve_blueprint.route('/reserve/command/edit', methods=['POST'])
def editReservation():
    # 获取前端传来的数据
    reservation_id = request.json.get('reservation_id')
    doctor_id = request.json.get('doctorId')
    patient_id = request.json.get('patientId')
    reserve_time = request.json.get('time')
    title = request.json.get('title')
    rank = request.json.get('rank')
    description = request.json.get('description')
    query_reservation = Reserve.query.filter(Reserve.id == reservation_id).first()
    if query_reservation is None:
        return {
            'code': 0,
            'message': '该记录不存在'
        }

    # 检查医生是否存在
    doctor = User.query.filter_by(id=doctor_id).first()
    if doctor is None:
        return {
            'code': 0,
            'message': '医生不存在'
        }
    # 检查患者是否存在
    patient = Patient.query.filter_by(id=patient_id).first()
    if patient is None:
        return {
            'code': 0,
            'message': '患者不存在'
        }
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    format_pattern = '%Y-%m-%d %H:%M:%S'
    # 检查时间是否合法
    if (datetime.datetime.strptime(str(reserve_time), format_pattern) - datetime.datetime.strptime(now_time,
                                                                                                   format_pattern)).days < 0:
        return {
            'code': 0,
            'message': '时间不合法'
        }

    query_reservation.doctor_id = doctor_id,
    query_reservation.patient_id = patient_id,
    query_reservation.reserve_time = reserve_time,
    query_reservation.title = title,
    query_reservation.description = description,
    query_reservation.rank = rank,
    query_reservation.operator_id = doctor_id,
    db.session.add(query_reservation)
    try:
        db.session.commit()
        return {
            'code': 1,
            'message': '修改预约成功'
        }
    except Exception as e:
        print(e)
        return {
            'code': 0,
            'message': '修改预约失败',
            'error': str(e)
        }
