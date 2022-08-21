from flask import request, make_response
from . import api
from app.utils.jwt_token import validate_token
from app.service.log_service import add_log_service, search_log_service
import logging

root_path = "/log"
logger = logging.getLogger(__name__)

@api.route(root_path, methods=['POST'])
@validate_token
def add_log():
    data = request.get_json()
    logger.info(f"log data: {data}")
    message = ""
    status = 200
    try:
        data['ip'] = request.remote_addr
        add_log_service(data)
        message = "success"
        logger.info(message)
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = errMessage
    response = make_response({"message": message}, status)
    return response

@api.route(f'{root_path}/<start>/<end>', methods=['GET'])
@validate_token
def search_log(start, end):
    result = []
    message = ""
    status = 200
    try:
        result = search_log_service(start, end)
        message = "查詢Log成功"
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "查詢Log失敗，請稍後再試"
    response = make_response({"message": message, "data": result}, status)
    return response