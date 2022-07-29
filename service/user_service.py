from model.user import User
from utils.password_encryption import encrypt_password, compare_passwords
from datetime import datetime, timedelta, timezone


def signup_service(userdata):
    user_id_check = User.objects[:1](user_id=userdata['user_id'])
    if user_id_check:
        raise Exception('此帳號已被註冊')
    else:
        user_id = userdata['user_id']
        gender = userdata['gender']
        email = userdata['email']
        height = userdata['height']
        weight = userdata['weight']
        birthday = userdata['birthday']
        role = userdata['role']
        password = encrypt_password(userdata['password'])
        create_time = datetime.now(timezone(timedelta(hours=+8)))

        user = User(user_id=user_id, gender=gender, height=height, weight=weight,
                    birthday=birthday, email=email, password=password, role=role, create_time=create_time)
        user.save()

def login_service(userdata):
    user_check = User.objects[:1](user_id=userdata['user_id'])
    if not user_check:
        raise Exception('查無此帳號')
    else:
        for user in user_check:
            return compare_passwords(userdata['password'], user['password'])

def search_service():
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
        user_data['create_time'] = user.create_time.strftime("%Y-%m-%d %H:%M:%S")
        user_data['update_time'] = "" if user.update_time is None else user.update_time.strftime("%Y-%m-%d %H:%M:%S")
        users.append(user_data)
        
    return users

def get_by_id_service(user_id):
    users = []
    for user in User.objects[:1](user_id=user_id):
        user_data = {}
        user_data['_id'] = str(user.id)
        user_data['user_id'] = user.user_id
        user_data['email'] = user.email
        user_data['height'] = user.height
        user_data['weight'] = user.weight
        user_data['gender'] = user.gender.description
        user_data['birthday'] = user.birthday
        user_data['role'] = user.role.description
        user_data['create_time'] = user.create_time.strftime("%Y-%m-%d %H:%M:%S")
        user_data['update_time'] = "" if user.update_time is None else user.update_time.strftime("%Y-%m-%d %H:%M:%S")
        users.append(user_data)
    return users