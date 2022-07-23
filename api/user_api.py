from flask import Blueprint, request, make_response
from service.user_service import signup_service, search_service, get_by_id_service, login_service
import logging

user_route = Blueprint('user_route', __name__)
root_path = "/api/user"
logger = logging.getLogger(__name__)

# 使用者註冊
@user_route.route(f"{root_path}/signup", methods=['POST'])
def signup():
    data = request.get_json()
    message = ""
    status = 200
    logger.info(f"{data['user_id']} 使用者註冊: {data}")
    try:
        signup_service(data)
        message = "註冊成功"
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "註冊失敗，請稍後再試"
    response = make_response({"message": message}, status)
    return response

# 使用者登入
@user_route.route(f"{root_path}/login", methods=['POST'])
def login():
    data = request.get_json()
    message = ""
    status = 200
    logger.info(f"{data['user_id']} 使用者登入")
    try:
        message = "登入成功" if login_service(data) else "登入失敗，帳號或密碼錯誤"
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "登入失敗，請稍後再試"
    response = make_response({"message": message}, status)
    return response

# 查詢所有使用者
@user_route.route(root_path, methods=['GET'])
def search():
    logger.info('user search')
    result = []
    message = ""
    status = 200
    try:
        result = search_service()
        message = "查詢成功"
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "查詢失敗，請稍後再試"
    response = make_response({"message": message, "data": result}, status)
    return response

# 依ID查詢使用者
@user_route.route(f"{root_path}/<user_id>", methods=['GET'])
def get_by_id(user_id):
    result = []
    message = ""
    status = 200
    try:
        result = get_by_id_service(user_id)
        message = "查詢成功"
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "查詢失敗，請稍後再試"
    response = make_response({"message": message, "data": result}, status)
    return response