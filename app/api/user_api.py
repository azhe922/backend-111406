from flask import request, make_response
from app.service.user_service import user_signup, user_search, getuser_by_id, user_login
import logging
from . import api
from app.utils.jwt_token import validate_token

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
        user_signup(data)
        message = "註冊成功"
        logger.info(f"{data['user_id']} {message}")
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "註冊失敗，請稍後再試"
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
        token = user_login(data)
        message = "登入成功" if token else "登入失敗，帳號或密碼錯誤"
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "登入失敗，請稍後再試"
    response = make_response({"message": message}, status)
    response.headers['token'] = token
    return response

# 查詢所有使用者


@api.route(root_path, methods=['GET'])
@validate_token
def search():
    result = []
    message = ""
    status = 200
    try:
        result = user_search()
        message = "查詢成功"
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "查詢失敗，請稍後再試"
    response = make_response({"message": message, "data": result}, status)
    return response

# 依ID查詢使用者


@api.route(f"{root_path}/<user_id>", methods=['GET'])
@validate_token
def get_by_id(user_id):
    result = []
    message = ""
    status = 200
    try:
        result = getuser_by_id(user_id)
        message = "查詢成功"
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "查詢失敗，請稍後再試"
    response = make_response({"message": message, "data": result}, status)
    return response
