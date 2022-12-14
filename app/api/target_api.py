from flask import request, make_response
from http import HTTPStatus
import logging
from . import api
from app.utils.jwt_token import validate_token
from app.service.target_service import add_target_service, get_target_service, update_actual_times_and_return, check_target_existed_service, check_target_isjuststarted_service, add_todo_service
from app.utils.backend_error import BackendException, UserTodoHasAlreadyCreateException
from flasgger import swag_from
from app.api.api_doc import target_get as get_doc

root_path = "/target"
logger = logging.getLogger(__name__)

# 新增個人計劃表


@api.route(root_path, methods=['POST'])
@validate_token(check_inperson=True)
def add_target():
    data = request.get_json()
    try:
        add_target_service(data)
        message = "新增訓練計劃表成功"
        logger.info(message)
        return make_response({"message": message}, HTTPStatus.OK)
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
    try:
        result = get_target_service(user_id)
        message = "查詢訓練計劃表成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)


@api.route(f"{root_path}/<user_id>/<target_date>", methods=['POST'])
@validate_token(check_inperson=True)
def update_target(user_id, target_date):
    data = request.get_json()
    try:
        result = update_actual_times_and_return(user_id, target_date, data)
        message = "更新訓練計劃表成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
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
    try:
        result = check_target_existed_service(user_id)
        message = "確認訓練表成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)


# 檢查是否為剛建立的訓練表
@api.route(f"{root_path}/started/<user_id>", methods=['GET'])
@validate_token()
def check_target_is_juststarted(user_id):
    try:
        result = check_target_isjuststarted_service(user_id)
        message = "確認訓練表成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)


@api.route(f"{root_path}/add/todo", methods=['POST'])
@validate_token(check_inperson=True)
def add_todo():
    try:
        data = request.get_json()
        user_id = data['user_id']
        target_date = data['target_date']
        result = add_todo_service(user_id, target_date)
        message = "新增訓練任務成功"
        logger.info(message)
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case UserTodoHasAlreadyCreateException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)