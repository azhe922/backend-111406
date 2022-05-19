from flask import Blueprint, request
from service.record_service import add_record_service, search_service

record_route = Blueprint('record_route', __name__)
root_path = "/api/record"

@record_route.route(root_path, methods=['POST'])
def add():
    data = request.get_json()
    return add_record_service(data)


@record_route.route(f"{root_path}/<user_id>", methods=['GET'])
def search(user_id):
    return search_service(user_id)
