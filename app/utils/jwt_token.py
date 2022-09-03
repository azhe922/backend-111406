import jwt
import os
from flask import make_response, request
from functools import wraps
from app.utils.backend_error import TokenNotProvidedException, AuthNotEnoughException, InvalidTokenProvidedException
from app.enums.user_role import UserRole

secret = os.getenv('token_secret')


def generate_token(payload):
    return jwt.encode(payload, secret, algorithm="HS256")


def validate_token(original_function=None, *, has_role=None, check_inperson=None):
    def _decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                token = request.headers['token']
            except Exception as e:
                (body, status) = TokenNotProvidedException.get_response_data()
                return make_response(body, status)

            try:
                payload = jwt.decode(token, secret, algorithms=["HS256"])
                user_role = payload['role']
                user_id = payload['user_id']

                # 使用者權限判斷
                if has_role:
                    if user_role < has_role:
                        (body, status) = AuthNotEnoughException.get_response_data()
                        return make_response(body, status)

                # 非管理員之角色才須個別判斷
                if user_role != UserRole.manager.value:
                    current_path = request.path
                    # 是否為本人
                    if check_inperson:
                        if user_id not in current_path and user_role < UserRole.doctor.value:
                            (body, status) = AuthNotEnoughException.get_response_data()
                            return make_response(body, status)

                return function(*args, **kwargs)
            except Exception as e:
                (body, status) = InvalidTokenProvidedException.get_response_data()
                return make_response(body, status)
        return wrapper

    # server啟動時會先將api內的裝飾器註冊一遍，沒有以下這行他會出名字重複的錯誤
    if original_function:
        _decorate.__name__ = original_function.__name__
    return _decorate
