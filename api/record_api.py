from flask import Blueprint, request
from service.record_service import add_record_service

record_route = Blueprint('record_route', __name__)
root_path = "/api/record"

@record_route.route(root_path, methods=['POST'])
def add():
    data = request.get_json()
    return add_record_service(data)
