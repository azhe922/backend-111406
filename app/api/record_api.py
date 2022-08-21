from flask import request, make_response
from app.service.record_service import add_record_service, search_record_service, get_standard_times_service
import logging
from . import api
from app.utils.jwt_token import validate_token

root_path = "/record"
logger = logging.getLogger(__name__)

# 新增運動測試紀錄


@api.route(root_path, methods=['POST'])
@validate_token
def add_record():
    data = request.get_json()
    logger.info(f"record data: {data}")
    message = ""
    status = 200
    try:
        analyze = __analyze_record(data)
        data['pr'] = analyze['pr']
        data['test_result'] = analyze['test_result']
        data.pop('gender', None)
        data.pop('age', None)
        add_record_service(data)
        data.pop('angles', None)
        message = "新增紀錄成功"
        logger.info(message)
    except Exception as e:
        data = {}
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "新增紀錄失敗，請稍後再試"
    response = make_response({"message": message, "data": data}, status)
    return response

# 查詢所有測試紀錄


@api.route(f"{root_path}/<user_id>", methods=['GET'])
@validate_token
def search_record(user_id):
    result = []
    message = ""
    status = 200
    try:
        result = search_record_service(user_id)
        message = "查詢成功"
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "查詢失敗，請稍後再試"
    response = make_response({"message": message, "data": result}, status)
    return response

# 測試結果數據分析


def __analyze_record(data):
    # the parameters like (user_id, age, part, gender, times)
    data = request.get_json()
    result = {}
    try:
        standard = get_standard_times_service(data)
        record = search_record_service(data['user_id'], True)
        times = data['times']
        compare = [s for s in standard if times >= s]
        difference = times - record[0]['times'] if len(record) > 0 else -999
        pr = len(compare) * 5
        test_result = ""
        if pr > 75:
            test_result = "很棒"
        elif pr > 20:
            test_result = "正常"
        else:
            test_result = "待加強"

        result = {
            "times": times,
            "pr": pr,
            "test_result": test_result
        }
        if difference > -100:
            result["difference"] = difference
        message = "分析成功"
        logger.info(message)
    except Exception as e:
        errMessage = str(e)
        logger.error(errMessage)
        raise Exception(e)
    return result
