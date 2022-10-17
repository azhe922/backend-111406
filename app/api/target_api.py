from flask import request, make_response
import logging
from . import api
from app.utils.jwt_token import validate_token
from app.service.target_service import add_target_service, get_target_service, update_target_times_service, check_target_existed_service, check_target_isjuststarted_service, add_todo_service
from app.utils.backend_error import BackendException, UserTodoHasAlreadyCreateException
from flasgger import swag_from
from app.api.api_doc import target_get as get_doc

root_path = "/target"
logger = logging.getLogger(__name__)

# 新增個人計劃表


@api.route(root_path, methods=['POST'])
@validate_token()
def add_target():
    data = request.get_json()
    message = ""
    status = 200
    try:
        add_target_service(data)
        message = "新增訓練計劃表成功"
        logger.info(message)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    return make_response({"message": message}, status)

# 查詢個人計劃表


@api.route(f"{root_path}/<user_id>", methods=['GET'])
@validate_token()
@swag_from(get_doc)
def get_target(user_id):
    """查詢個人計劃表
    """
    result = []
    message = ""
    status = 200
    try:
        result = get_target_service(user_id)
        message = "查詢訓練計劃表成功"
        logger.info(message)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    return make_response({"message": message, "data": result}, status)


@api.route(f"{root_path}/<user_id>/<target_date>", methods=['POST'])
@validate_token(check_inperson=True)
def update_target(user_id, target_date):
    data = request.get_json()
    message = ""
    status = 200
    try:
        update_target_times_service(user_id, target_date, data)
        message = "更新訓練計劃表成功"
        logger.info(message)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    return make_response({"message": message}, status)


@api.route(f"{root_path}/existed/<user_id>", methods=['GET'])
@validate_token()
def target_check_existed(user_id):
    result = False
    message = ""
    status = 200
    try:
        result = check_target_existed_service(user_id)
        message = "確認訓練表成功"
        logger.info(message)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    return make_response({"message": message, "data": result}, status)


# 檢查是否為剛建立的訓練表
@api.route(f"{root_path}/started/<user_id>", methods=['GET'])
@validate_token()
def check_target_is_juststarted(user_id):
    result = False
    message = ""
    status = 200
    try:
        result = check_target_isjuststarted_service(user_id)
        message = "確認訓練表成功"
        logger.info(message)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    return make_response({"message": message, "data": result}, status)


@api.route(f"{root_path}/add/todo/<user_id>", methods=['POST'])
@validate_token(check_inperson=True)
def add_todo(user_id):
    data = request.get_json()
    message = ""
    status = 200
    try:
        add_todo_service(user_id, data)
        message = "新增訓練任務成功"
        logger.info(message)
    except Exception as e:
        match e.__class__.__name__:
            case UserTodoHasAlreadyCreateException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    return make_response({"message": message}, status)