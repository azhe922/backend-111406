from app.model.validcode import ValidCode
from app.utils.backend_error import ExpiredOtpException, OtherOtpException
from app.utils.jwt_token import generate_token
from app.utils.backend_util import datetime_delta
from app.enums.deltatime_type import DeltaTimeType
import datetime
import time


def add_valid_code(data):
    email = data['email']
    deprecated_code = ValidCode.objects[:1](email=email)
    otp = data['otp']
    create_time = int(time.time())

    if deprecated_code:
        deprecated_code = deprecated_code.get(email=email)
        deprecated_code.otp = otp
        deprecated_code.create_time = create_time
        deprecated_code.save()
    else:
        validcode = ValidCode(email=email, otp=otp, create_time=create_time)
        validcode.save()


def get_code(email):
    otp = ""
    valid_time = int(time.time())
    valid_code = ValidCode.objects[:1](email=email)
    if valid_code:
        valid_code = valid_code.get(email=email)
        otp = valid_code.otp
        if valid_time - valid_code.create_time > 300:
            raise ExpiredOtpException()
    else:
        raise OtherOtpException()

    payload = {"email": email, 'exp': datetime_delta(
        datetime.datetime.utcnow(), key=DeltaTimeType.minutes, value=10)}
    token = generate_token(payload)
    return (otp, token)
