from flask import request, make_response
from app.service.record_service import add_record_service, get_record_before_last_target, get_standard_times_service, search_records_by_userid
from app.service.target_service import get_last_and_iscompleted_target, check_target_existed_service, check_target_isjuststarted_service
import logging
from . import api
from app.utils.jwt_token import validate_token
from app.utils.backend_error import BackendException
from flasgger import swag_from
from app.api.api_doc import record_search as search_doc_record

root_path = "/record"
logger = logging.getLogger(__name__)

# 新增運動測試紀錄


@api.route(root_path, methods=['POST'])
@validate_token()
def add_record():
    data = request.get_json()
    message = ""
    status = 200
    try:
        (analyze, has_record) = __analyze_record(data)
        data['pr'] = analyze['pr']
        data['test_result'] = analyze['test_result']
        data.pop('gender', None)
        data.pop('age', None)
        add_record_service(data)
        data.pop('angles', None)
        data['difference'] = analyze['difference'] if has_record else None
        message = "新增紀錄成功"
        logger.info(message)
    except Exception as e:
        data = {}
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    return make_response({"message": message, "data": data}, status)

# 查詢使用者所有測試紀錄


@api.route(f"{root_path}/<user_id>", methods=['GET'])
@validate_token(check_inperson=True)
@swag_from(search_doc_record)
def search_record(user_id):
    """查詢使用者所有測試紀錄
    """
    result = []
    message = ""
    status = 200
    try:
        result = search_records_by_userid(user_id)
        message = "查詢成功"
        logger.info(message)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    return make_response({"message": message, "data": result}, status)

# 測試結果數據分析


def __analyze_record(data):
    # the parameters like (user_id, age, part, gender, times)
    data = request.get_json()
    user_id = data['user_id']
    times = data['times']
    result = {}
    has_record = False
    difference = None
    # 取得常模分配表
    standard = get_standard_times_service(data)
    # 確認使用者的訓練計劃表是否正在執行
    check_ishad_existed_target = check_target_existed_service(user_id)
    # 確認使用者的訓練計劃表是不是剛開始
    check_isjuststarted_target = check_target_isjuststarted_service(user_id)
    # 取得使用者已做完的訓練中最近一筆的建立時間
    target_create_time = get_last_and_iscompleted_target(user_id)
    if target_create_time > 0 and not check_ishad_existed_target and not check_isjuststarted_target:
        # 取得前側紀錄
        record = get_record_before_last_target(data['user_id'], target_create_time, data['part'])
        difference = times - record['times']
    compare = [s for s in standard if times >= s]
    pr = len(compare) * 5
    test_result = ""
    if pr > 75:
        test_result = "很棒"
    elif pr > 20:
        test_result = "正常"
    else:
        test_result = "待加強"

    result = {
        "pr": pr,
        "test_result": test_result
    }
    if difference:
        has_record = True
        result["difference"] = difference
    logger.info("分析成功")
    return (result, has_record)
