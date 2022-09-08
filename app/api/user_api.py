from flask import request, make_response
from app.service.user_service import user_signup_service, search_user_service, getuser_by_id_service, user_login_service, update_user_service, update_pwd_service
import logging
from . import api
from app.utils.jwt_token import validate_token, validate_change_forget_pwd_token
from app.utils.backend_error import LoginFailedException, BackendException, UserIdOrEmailAlreadyExistedException, NotFoundUseridException, PasswordIncorrectException

root_path = "/user"
logger = logging.getLogger(__name__)

# 使用者註冊


@api.route(f"{root_path}/signup", methods=['POST'])
def signup():
    data = request.get_json()
    message = ""
    status = 200
    logger.info(f"{data['user_id']} 使用者註冊: {data}")
    try:
        user_signup_service(data)
        message = "註冊成功"
        logger.info(f"{data['user_id']} {message}")
    except Exception as e:
        match e.__class__.__name__:
            case UserIdOrEmailAlreadyExistedException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    response = make_response({"message": message}, status)
    return response

# 使用者登入


@api.route(f"{root_path}/login", methods=['POST'])
def login():
    data = request.get_json()
    message = ""
    status = 200
    token = ""
    logger.info(f"{data['user_id']} 使用者登入")
    try:
        token = user_login_service(data)
        message = "登入成功"
    except Exception as e:
        match e.__class__.__name__:
            case LoginFailedException.__name__ | NotFoundUseridException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    response = make_response({"message": message}, status)
    response.headers['token'] = token
    return response

# 查詢所有使用者


@api.route(root_path, methods=['GET'])
@validate_token(has_role=200)
def search_user():
    result = []
    message = ""
    status = 200
    try:
        result = search_user_service()
        message = "查詢成功"
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    response = make_response({"message": message, "data": result}, status)
    return response

# 依ID查詢使用者


@api.route(f"{root_path}/<user_id>", methods=['GET'])
@validate_token(check_inperson=True)
def getuser_by_id(user_id):
    result = []
    message = ""
    status = 200
    try:
        result = getuser_by_id_service(user_id)
        message = "查詢成功"
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    response = make_response({"message": message, "data": result}, status)
    return response

# 使用者資料更新


@api.route(f"{root_path}/update", methods=['POST'])
@validate_token(check_inperson=True)
def update_user():
    data = request.get_json()
    message = ""
    status = 200
    logger.info(f"{data['user_id']} 使用者資料更新: {data}")
    try:
        update_user_service(data)
        message = "更新成功"
        logger.info(f"{data['user_id']} {message}")
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    response = make_response({"message": message}, status)
    return response

# 修改密碼


@api.route(f"{root_path}/update/password", methods=['POST'])
@validate_token(check_inperson=True)
def update_pwd():
    data = request.get_json()
    message = ""
    status = 200
    logger.info(f"{data['user_id']} 修改密碼")
    try:
        update_pwd_service(data)
        message = "更新成功"
        logger.info(message)
    except Exception as e:
        match e.__class__.__name__:
            case PasswordIncorrectException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    response = make_response({"message": message}, status)
    return response

# 忘記密碼修改


@api.route(f"{root_path}/update/forget/password", methods=['POST'])
@validate_change_forget_pwd_token
def update_forget_pwd():
    data = request.get_json()
    message = ""
    status = 200
    logger.info(f"{data['email']} 修改密碼")
    try:
        update_pwd_service(data)
        message = "更新成功"
        logger.info(message)
    except Exception as e:
        match e.__class__.__name__:
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    response = make_response({"message": message}, status)
    return response
