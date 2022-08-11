from app.model.user import User
from app.utils.password_encryption import encrypt_password, compare_passwords
import time
from datetime import datetime as dt
import datetime
from app.utils.jwt_token import generate_token
import json


def signup(userdata):
    user_id_check = User.objects[:1](user_id=userdata['user_id'])
    if user_id_check:
        raise Exception('此帳號已被註冊')
    else:
        userdata['password'] = encrypt_password(userdata['password'])
        userdata['create_time'] = int(time.time())

        user = json.loads(userdata, object_hook=lambda d: User(**d))
        user.save()


def login(userdata):
    user_check = User.objects[:1](user_id=userdata['user_id'])
    if not user_check:
        raise Exception('查無此帳號')
    else:
        for user in user_check:
            payload = {"user_id": user['user_id'], "_id": str(user['id']),
                       "email": user['email'], "role": user['role'].value, 
                       'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}
            print(payload)
            if compare_passwords(userdata['password'], user['password']):
                return generate_token(payload)
            else:
                return None


def search():
    users = []
    for user in User.objects:
        user_data = {}
        user_data['_id'] = str(user.id)
        user_data['user_id'] = user.user_id
        user_data['email'] = user.email
        user_data['height'] = user.height
        user_data['weight'] = user.weight
        user_data['gender'] = user.gender.description
        user_data['birthday'] = user.birthday
        user_data['role'] = user.role.description
        user_data['create_time'] = dt.fromtimestamp(
            user.create_time).strftime('%Y-%m-%d %H:%M:%S')
        user_data['update_time'] = "" if user.update_time is None else dt.fromtimestamp(
            user.update_time).strftime('%Y-%m-%d %H:%M:%S')
        users.append(user_data)

    return users


def get_by_id(user_id):
    users = []
    for user in User.objects[:1](user_id=user_id):
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['email'] = user.email
        user_data['height'] = user.height
        user_data['weight'] = user.weight
        user_data['gender'] = user.gender.description
        user_data['birthday'] = user.birthday
        user_data['role'] = user.role.description
        user_data['create_time'] = dt.fromtimestamp(
            user.create_time).strftime('%Y-%m-%d %H:%M:%S')
        user_data['update_time'] = "" if user.update_time is None else dt.utcfromtimestamp(
            user.update_time).strftime('%Y-%m-%d %H:%M:%S')
        users.append(user_data)
    return users
