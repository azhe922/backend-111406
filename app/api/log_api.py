from http import HTTPStatus
from flask import request, make_response
from . import api
from app.utils.jwt_token import validate_token
from app.service.log_service import add_log_service, search_log_service
from app.utils.backend_error import BackendException
import logging

root_path = "/log"
logger = logging.getLogger(__name__)

@api.route(root_path, methods=['POST'])
@validate_token()
def add_log():
    data = request.get_json()
    logger.info(f"log data: {data}")
    try:
        data['ip'] = request.remote_addr
        add_log_service(data)
        message = "success"
        logger.info(message)
        return make_response({"message": message}, HTTPStatus.OK)
    except Exception as e:
        logger.error(str(e))
        e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

@api.route(f'{root_path}/<start>/<end>', methods=['GET'])
@validate_token()
def search_log(start, end):
    try:
        result = search_log_service(start, end)
        message = "查詢Log成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        logger.error(str(e))
        e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)