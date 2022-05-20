from model.user import User
from flask import make_response
from utils.passwordEncryption import encrypt_password
from datetime import datetime, timedelta, timezone


def signup_service(userdata):
    try:
        user_id_check = User.objects[:1](user_id=userdata['user_id'])
        if user_id_check:
            return {"status": 404, "message": "UserId already exists"}
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

            return make_response({'message': 'succesfully inserted'}, 200)

    except Exception as e:
        return make_response({'message': str(e)}, 500)


def search_service():
    users = []
    try:
        for user in User.objects:
            user_data = {}
            user_data['_id'] = str(user.id)
            user_data['user_id'] = user.user_id
            user_data['email'] = user.email
            user_data['height'] = user.height
            user_data['weight'] = user.weight
            user_data['gender'] = user.gender
            user_data['birthday'] = user.birthday
            user_data['role'] = user.role
            users.append(user_data)

        return make_response({'message': '查詢成功', 'data': users}, 200)

    except Exception as e:
        return make_response({'message': str(e)}, 500)
