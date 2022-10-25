from flask import request, make_response
from http import HTTPStatus
from app.service.user_service import update_user_service_ethsum, user_signup_service, search_user_service, getuser_by_id_service, user_login_service, update_user_service, update_pwd_service, update_forget_pwd_service
import logging
from . import api
from app.utils.jwt_token import validate_token, validate_change_forget_pwd_token
from app.utils.backend_error import LoginFailedException, BackendException, UserIdOrEmailAlreadyExistedException, NotFoundUseridException, PasswordIncorrectException
from flasgger import swag_from
from app.api.api_doc import user_signup as signup_doc, user_login as login_doc, user_search as search_doc, user_get as get_doc

root_path = "/user"
logger = logging.getLogger(__name__)

# 使用者註冊


@api.route(f"{root_path}/signup", methods=['POST'])
@swag_from(signup_doc)
def signup():
    """使用者註冊
    """
    data = request.get_json()
    logger.info(f"{data['user_id']} 使用者註冊: {data}")
    try:
        user_signup_service(data)
        message = "註冊成功"
        logger.info(f"{data['user_id']} {message}")
        return make_response({"message": message}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case UserIdOrEmailAlreadyExistedException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 使用者登入


@api.route(f"{root_path}/login", methods=['POST'])
@swag_from(login_doc)
def login():
    """使用者登入    
    """
    data = request.get_json()
    logger.info(f"{data['user_id']} 使用者登入")
    try:
        token = user_login_service(data)
        message = "登入成功"        
        response = make_response({"message": message}, HTTPStatus.OK)
        response.headers['token'] = token
        return response
    except Exception as e:
        match e.__class__.__name__:
            case LoginFailedException.__name__ | NotFoundUseridException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 查詢所有使用者


@api.route(root_path, methods=['GET'])
@validate_token(has_role=200)
@swag_from(search_doc)
def search_user():
    """查詢所有使用者
    需要管理者帳號才能使用
    """
    try:
        result = search_user_service()
        message = "查詢成功"
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)    

# 依ID查詢使用者


@api.route(f"{root_path}/<user_id>", methods=['GET'])
@validate_token(check_inperson=True)
@swag_from(get_doc)
def getuser_by_id(user_id):
    """依使用者ID查詢用戶資料
    """
    try:
        result = getuser_by_id_service(user_id)
        message = "查詢成功"
        return make_response({"message": message, "data": result}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 使用者資料更新


@api.route(f"{root_path}/update/<user_id>", methods=['POST'])
@validate_token(check_inperson=True)
def update_user(user_id):
    data = request.get_json()
    logger.info(f"{user_id} 使用者資料更新: {data}")
    try:
        update_user_service(data, user_id)
        message = "更新成功"
        logger.info(f"{user_id} {message}")
        return make_response({"message": message}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 使用者代幣更新

@api.route(f"{root_path}/ethupdate/<user_id>", methods=['POST'])
@validate_token(check_inperson=True)
def update_user_eth(user_id):
    data = request.get_json()
    logger.info(f"{user_id} 使用者代幣更新: {data}")
    try:
        update_user_service_ethsum(data, user_id)
        message = "更新成功"
        logger.info(f"{user_id} {message}")
        return make_response({"message": message}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 修改密碼


@api.route(f"{root_path}/update/password", methods=['POST'])
@validate_token(check_inperson=True)
def update_pwd():
    data = request.get_json()
    logger.info(f"{data['user_id']} 修改密碼")
    try:
        update_pwd_service(data)
        message = "更新成功"
        logger.info(message)
        return make_response({"message": message}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case PasswordIncorrectException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)

# 忘記密碼修改


@api.route(f"{root_path}/update/forget/password", methods=['POST'])
@validate_change_forget_pwd_token
def update_forget_pwd():
    data = request.get_json()
    logger.info(f"{data['email']} 修改密碼")
    try:
        update_forget_pwd_service(data)
        message = "更新成功"
        logger.info(message)
        return make_response({"message": message}, HTTPStatus.OK)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
        return make_response({"message": message}, status)
