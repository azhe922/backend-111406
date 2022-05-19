from flask import Blueprint, request
from service.user_service import signup_service, search_service

user_route = Blueprint('user_route', __name__)
root_path = "/api/user"

@user_route.route(f"{root_path}/signup", methods=['POST'])
def signup():
    data = request.get_json()
    return signup_service(data)

@user_route.route(root_path, methods=['GET'])
def search():
    return search_service()