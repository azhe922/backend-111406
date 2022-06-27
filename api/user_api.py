from flask import Blueprint, request, make_response
from service.user_service import signup_service, search_service, get_by_id_service, login_service

user_route = Blueprint('user_route', __name__)
root_path = "/api/user"

@user_route.route(f"{root_path}/signup", methods=['POST'])
def signup():
    data = request.get_json()
    message = ""
    status = 200
    try:
        signup_service(data)
        message = "註冊成功"
    except Exception as e:
        message = str(e)
        status = 500
    response = make_response({"message": message}, status)
    return response

@user_route.route(f"{root_path}/login", methods=['POST'])
def login():
    data = request.get_json()
    message = ""
    status = 200
    try:
        message = "登入成功" if login_service(data) else "登入失敗，帳號或密碼錯誤"
    except Exception as e:
        message = str(e)
        status = 500
    response = make_response({"message": message}, status)
    return response

@user_route.route(root_path, methods=['GET'])
def search():
    result = []
    message = ""
    status = 200
    try:
        result = search_service()
        message = "查詢成功"
    except Exception as e:
        message = str(e)
        status = 500
    response = make_response({"message": message, "data": result}, status)
    return response

@user_route.route(f"{root_path}/<user_id>", methods=['GET'])
def get_by_id(user_id):
    result = []
    message = ""
    status = 200
    try:
        result = get_by_id_service(user_id)
        message = "查詢成功"
    except Exception as e:
        message = str(e)
        status = 500
    response = make_response({"message": message, "data": result}, status)
    return response