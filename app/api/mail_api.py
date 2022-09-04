from flask import request, make_response
from flask_mail import Message
import logging
from threading import Thread
from app import mail
from . import api
from random import randint
from app.service.mail_service import get_code, add_valid_code
from app.service.user_service import check_email_existed
from app.utils.backend_error import BackendException, IncorrectOtpException, ExpiredOtpException, OtherOtpException, NotFoundEmailException
root_path = "/mail"
logger = logging.getLogger(__name__)
message = ""


# 發送驗證碼
@api.route(f"{root_path}/code", methods=['POST'])
def send_validcode_mail():
    data = request.get_json()
    otp = ''.join([str(randint(0, 9)) for k in range(0, 6)])
    logger.info(f"email data: {data}")
    valid_body = f"您的驗證碼: {otp}"
    valid_title = "忘記密碼驗證信"
    try:
        email = data['email']
        data['otp'] = otp
        check_email_existed(email)

        #  使用多執行緒
        from application import app
        thr = Thread(target=__send_async_email, args=[
                     app, valid_title, email, valid_body])
        thr.start()

        add_valid_code(data)
        status = 200
        message = "郵件發送成功"
        logger.info(message)
    except Exception as e:
        match e.__class__.__name__:
            case NotFoundEmailException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    response = make_response({"message": message}, status)
    return response


@api.route(f'{root_path}/validate', methods=["POST"])
def validate():
    data = request.get_json()
    try:
        otp = get_code(data['email'])
        message = "驗證成功" if otp == data['otp'] else "驗證碼錯誤"
        status = 200         
        logger.info(message)
    except Exception as e:
        match e.__class__.__name__:
            case IncorrectOtpException.__name__ | ExpiredOtpException.__name__ | OtherOtpException.__name__:
                pass
            case _:
                logger.error(str(e))
                e = BackendException()
        (message, status) = e.get_response_message()
    response = make_response({"message": message}, status)
    return response


def __send_async_email(app, valid_title, email, valid_body):
    msg = Message(valid_title,
                  sender="10846006@ntub.edu.tw",
                  # recipients 必須為陣列格式
                  recipients=[email],
                  body=valid_body)
    with app.app_context():
        mail.send(msg)
