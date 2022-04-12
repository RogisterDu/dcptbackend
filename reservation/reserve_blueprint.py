import calendar
import datetime

from flask import Blueprint, request
from sqlalchemy import and_, text

from patient.model import Patient
from user.model import User
from .model import Reserve

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
            'type': status_list[item[0].rank],
            'rank': item[0].rank,
            'title': item[0].title,
            'time': datetime.datetime.strptime(str(item[0].reserve_time), "%Y-%m-%d %H:%M:%S").strftime(
                "%Y-%m-%d %H:%M:%S"),
            'doctor_Id': item[0].doctor_id,
            'doctorName': item[1].realName,
            'patientId': item[0].patient_id,
            'patientName': item[2].name,
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
            'type': status_list[item[0].rank],
            'rank': item[0].rank,
            'title': item[0].title,
            'time': datetime.datetime.strptime(str(item[0].reserve_time), "%Y-%m-%d %H:%M:%S").strftime(
                "%Y-%m-%d %H:%M:%S"),
            'doctor_Id': item[0].doctor_id,
            'doctorName': item[1].realName,
            'patientId': item[0].patient_id,
            'patientName': item[2].name,
        })
    return {
        'code': 1,
        'data': return_result,
        'message': '查询成功'
    }
