from flask import request, make_response
from flask_mail import Message
import logging
from threading import Thread
from app import mail
from . import api
from random import randint
from app.service.mail_service import get_code, add_valid_code
from app.service.user_service import check_email_existed

root_path = "/mail"
logger = logging.getLogger(__name__)
message = ""


# 發送驗證碼
@api.route(f"{root_path}/code", methods=['POST'])
def send_mail():
    data = request.get_json()
    otp = ''.join([str(randint(0,9)) for k in range(0, 6)])
    logger.info(f"email data: {data}")
    valid_body = f"您的驗證碼: {otp}"
    valid_title = "忘記密碼驗證信"
    try:
        email = data['email']
        data['otp'] = otp
        check_email_existed(email)
        
        #  使用多執行緒
        from application import app
        thr = Thread(target=__send_async_email, args=[app, valid_title, email, valid_body])
        thr.start()
        
        add_valid_code(data)
        status = 200
        message = "郵件發送成功"
        logger.info(message)
    except Exception as e:
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "郵件發送失敗，請稍後再試"
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
        errMessage = str(e)
        status = 500
        logger.error(errMessage)
        message = "驗證碼過期，請重新驗證" if "expired" in errMessage else "驗證失敗，請稍後再試"
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
