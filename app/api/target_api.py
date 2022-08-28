from flask import request, make_response
import logging
from . import api
from app.utils.jwt_token import validate_token
from app.service.target_service import add_target_service, get_target_service, update_target_times_service

root_path = "/target"
logger = logging.getLogger(__name__)

# 新增個人計劃表


@api.route(root_path, methods=['POST'])
@validate_token
def add_target():
    data = request.get_json()
    logger.info(f"target data: {data}")
    message = ""
    status = 200
    try:
        add_target_service(data)
        message = "新增訓練計劃表成功"
        logger.info(message)
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "新增訓練計劃表失敗，請稍後再試"
    response = make_response({"message": message}, status)
    return response

# 查詢個人計劃表


@api.route(f"{root_path}/<user_id>", methods=['GET'])
@validate_token
def get_target(user_id):
    result = {}
    message = ""
    status = 200
    try:
        result = get_target_service(user_id)
        message = "查詢訓練計劃表成功"
        logger.info(message)
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "查詢訓練計劃表失敗，請稍後再試"
    response = make_response({"message": message, "data": result}, status)
    return response

@api.route(f"{root_path}/<user_id>/<target_date>", methods=['PATCH'])
@validate_token
def update_target(user_id, target_date):
    data = request.get_json()
    result = {}
    message = ""
    status = 200
    try:
        update_target_times_service(user_id, target_date, data)
        message = "更新訓練計劃表成功"
        logger.info(message)
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "更新訓練計劃表失敗，請稍後再試"
    response = make_response({"message": message}, status)
    return response