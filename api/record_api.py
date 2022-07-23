from flask import Blueprint, request, make_response
from service.record_service import add_record_service, search_service
import logging

record_route = Blueprint('record_route', __name__)
root_path = "/api/record"
logger = logging.getLogger(__name__)

# 新增運動紀錄
@record_route.route(root_path, methods=['POST'])
def add():
    data = request.get_json()
    message = ""
    status = 200
    try:
        add_record_service(data)
        message = "新增紀錄成功"
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "新增紀錄失敗，請稍後再試"
    response = make_response({"message": message}, status)
    return response

# 查詢所有運動紀錄
@record_route.route(f"{root_path}/<user_id>", methods=['GET'])
def search(user_id):
    result = []
    message = ""
    status = 200
    try:
        result = search_service(user_id)
        message = "查詢成功"
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "查詢失敗，請稍後再試"
    response = make_response({"message": message, "data": result}, status)
    return response
