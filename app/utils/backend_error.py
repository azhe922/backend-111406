from email import message


class BackendException(Exception):
    def __init__(self) -> None:
        pass

    @classmethod
    def get_response_data(self):
        return (self.message, self.status)


class TokenNotProvidedException(BackendException):
    """
    未提供 token
    """
    message = {"message": "Token not provided"}
    status = 403

class AuthNotEnoughException(BackendException):
    """
    權限不足
    """
    message = {"message": "Authentication is not enough"}
    status = 403


class InvalidTokenProvidedException(BackendException):
    """
    token 格式錯誤
    """
    message = {"message": "Invalid token provided"}
    status = 403

class LoginFailedException(BackendException):
    message = {"message": "登入失敗，帳號或密碼錯誤"}
    status = 500