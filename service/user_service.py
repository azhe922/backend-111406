from model.user import User
from flask import make_response
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
            user_data['sex'] = user.sex
            user_data['birthday'] = user.birthday
            user_data['role'] = user.role
            users.append(user_data)

        return make_response({'message': 'succesfully inserted', 'data': users}, 200)

    except Exception as e:
        return make_response({'message': str(e)}, 404)