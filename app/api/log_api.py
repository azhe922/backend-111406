from http import HTTPStatus
from flask import request, make_response
from http import HTTPStatus
from . import api
from app.service.log_service import add_log_service
from app.utils.backend_error import BackendException
import logging

root_path = "/log"
logger = logging.getLogger(__name__)

@api.route(root_path, methods=['POST'])
def add_log():
    data = request.get_json()
    logger.info(f"log data: {data}")
    try:
        data['ip'] = request.remote_addr
        add_log_service(data)
        message = "log success"
        logger.info(message)
        return make_response({"message": message}, HTTPStatus.OK)
    except Exception as e:
        logger.error(str(e))
        e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)