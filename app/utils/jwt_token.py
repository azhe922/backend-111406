import os
import logging
from flask import make_response, request, g
from functools import wraps
from app.utils.backend_error import TokenNotProvidedException, AuthNotEnoughException, InvalidTokenProvidedException
from app.enums.user_role import UserRole
from jwt import ExpiredSignatureError, encode, decode

secret = os.getenv('token_secret')
logger = logging.getLogger(__name__)


def generate_token(payload):
    return encode(payload, secret, algorithm="HS256")


def validate_token(original_function=None, *, has_role=None, check_inperson=None):
    def _decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                token = request.headers.get("token")
                if not token:
                    raise TokenNotProvidedException()
                payload = decode(token, secret, algorithms=["HS256"])

                # 使用者權限判斷
                __check_role(payload, has_role)

                # 非管理員之角色才須個別判斷
                __check_inperson(payload, check_inperson)

                return function(*args, **kwargs)
            except ExpiredSignatureError:
                from app.service.user_service import check_user_token

                new_token = check_user_token(token)
                if new_token:
                    payload = decode(new_token, secret, algorithms=["HS256"])

                    # 使用者權限判斷
                    __check_role(payload, has_role)

                    # 非管理員之角色才須個別判斷
                    __check_inperson(payload, check_inperson)

                    g.token = new_token
                    return function(*args, **kwargs)
            except Exception as e:
                match (e.__class__.__name__):
                    case AuthNotEnoughException.__name__ | TokenNotProvidedException.__name__:
                        pass
                    case _:
                        logger.error(str(e))
                        e = InvalidTokenProvidedException()
                (body, status) = e.get_response_body()
                return make_response(body, status)
        return wrapper

    # server啟動時會先將api內的裝飾器註冊一遍，沒有以下這行他會出名字重複的錯誤
    if original_function:
        _decorate.__name__ = original_function.__name__
    return _decorate


def validate_change_pwd_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get("token")
            if not token:
                raise TokenNotProvidedException()
            payload = decode(token, secret, algorithms=["HS256"])
            email = payload['email']
            json = request.get_json()

            if json['email'] != email:
                raise AuthNotEnoughException()

            return function(*args, **kwargs)
        except Exception as e:
            match (e.__class__.__name__):
                case AuthNotEnoughException.__name__ | TokenNotProvidedException.__name__:
                    pass
                case _:
                    e = InvalidTokenProvidedException()
            (body, status) = e.get_response_body()
            return make_response(body, status)
    return wrapper


def __check_role(payload, has_role):
    user_role = payload['role']
    if has_role:
        if user_role < has_role:
            raise AuthNotEnoughException()


def __check_inperson(payload, check_inperson):
    user_role = payload['role']
    user_id = payload['user_id']
    if user_role != UserRole.manager.value:
        current_path = request.path
        # 是否為本人
        if check_inperson:
            if user_id not in current_path and user_role < UserRole.doctor.value:
                raise AuthNotEnoughException()
