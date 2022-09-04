from app.model.user import User
from app.utils.password_encryption import encrypt_password, compare_passwords
import time
from datetime import datetime as dt
import datetime
from app.utils.jwt_token import generate_token
from app.utils.backend_util import dict_to_json, datetime_delta, datetime_strf
from app.utils.backend_error import NotFoundEmailException


def user_signup_service(userdata):
    user_id_check = User.objects[:1](user_id=userdata['user_id'])
    email_check = User.objects[:1](email=userdata['email'])
    if user_id_check | email_check:
        raise Exception('此帳號或email已被註冊')
    else:
        userdata['password'] = encrypt_password(
            userdata['password']).decode("utf-8")
        userdata['create_time'] = int(time.time())

        userdata_json = dict_to_json(userdata)
        user = User().from_json(userdata_json)
        user.save()


def user_login_service(userdata):
    user_check = User.objects[:1](user_id=userdata['user_id'])
    if not user_check:
        raise Exception('查無此帳號')
    else:
        for user in user_check:
            payload = {"user_id": user['user_id'], "_id": str(user['id']),
                       "email": user['email'], "role": user['role'].value,
                       'exp': datetime_delta(datetime.datetime.utcnow(), key='minutes', value=60)}
            if compare_passwords(userdata['password'], user['password']):
                return generate_token(payload)
            else:
                return None


def search_user_service():
    users = []
    for user in User.objects:
        user_data = user.to_json()
        user_data['create_time'] = datetime_strf(user.create_time)
        user_data['update_time'] = "" if user.update_time is None else datetime_strf(user.update_time)
        users.append(user_data)

    return users


def getuser_by_id_service(user_id):
    for user in User.objects[:1](user_id=user_id):
        user_data = user.to_json()
        user_data['create_time'] = datetime_strf(user.create_time)
        user_data['update_time'] = "" if user.update_time is None else datetime_strf(user.update_time)
        return user_data


def update_user_service(user):
    old_user = User.objects(user_id=user['user_id'])
    update_time = int(time.time())
    if old_user:
        old_user = old_user.get(user_id=user['user_id'])
        userdata_json = dict_to_json(user)
        new_user = User().from_json(userdata_json)
        old_user.email = new_user.email
        old_user.height = new_user.height
        old_user.weight = new_user.weight
        old_user.gender = new_user.gender
        old_user.birthday = new_user.birthday
        old_user.role = new_user.role
        old_user.update_time = update_time
        old_user.save()



def check_email_existed(email):
    email_check = User.objects[:1](email=email)
    if not email_check:
        raise NotFoundEmailException()
