from flask import Blueprint, request
from service.record_service import add_record_service

record_route = Blueprint('record_route', __name__)

@record_route.route("/api/record", methods=['POST'])
def add():
    data = request.get_json()
    return add_record_service(data)
