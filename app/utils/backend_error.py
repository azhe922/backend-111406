class BackendException(Exception):
    message = "伺服器端錯誤，請稍後再試"
    body = {"message": message}
    status = 500

    @classmethod
    def get_response_body(self):
        return (self.body, self.status)

    @classmethod
    def get_response_message(self):
        return (self.message, self.status)

    def __str__(self) -> str:
        return self.message


class TokenNotProvidedException(BackendException):
    """
    未提供 token
    """
    message = "Token not provided"
    body = {"message": message}
    status = 403


class AuthNotEnoughException(BackendException):
    """
    權限不足
    """
    message = "Authentication is not enough"
    body = {"message": message}
    status = 403


class InvalidTokenProvidedException(BackendException):
    """
    token 格式錯誤
    """
    message = "Invalid token provided"
    body = {"message": message}
    status = 403


class LoginFailedException(BackendException):
    message = "登入失敗，帳號或密碼錯誤"
    body = {"message": message}
    status = 500


class ExpiredOtpException(BackendException):
    message = "驗證碼過期，請重新驗證"
    body = {"message": message}
    status = 500


class IncorrectOtpException(BackendException):
    message = "驗證碼錯誤"
    body = {"message": message}
    status = 500


class OtherOtpException(BackendException):
    message = "請重新發送驗證碼"
    body = {"message": message}
    status = 500


class NotFoundEmailException(BackendException):
    message = "查無此email"
    body = {"message": message}
    status = 500


class NotFoundUseridException(BackendException):
    message = "查無此使用者帳號"
    body = {"message": message}
    status = 500


class UserIdOrEmailAlreadyExistedException(BackendException):
    message = "此帳號或email已被註冊"
    body = {"message": message}
    status = 500


class PasswordIncorrectException(BackendException):
    message = "輸入密碼與舊密碼不相符"
    body = {"message": message}
    status = 500


class UserTodoHasAlreadyCreateException(BackendException):
    message = "今天已經做過訓練任務囉！如果需要多做訓練請等待至隔日再新增任務！"
    body = {"message": message}
    status = 500
