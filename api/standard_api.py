from flask import Blueprint, make_response, request

from service.standard_service import get_times_service

standard_route = Blueprint('standard_route', __name__)
root_path = "/api/standard"

@standard_route.route(f"{root_path}/get/times", methods=['GET'])
def get_times():
    data = request.get_json()
    result = []
    message = ""
    status = 200
    try:
        result = get_times_service(data)
        message = "查詢成功"
    except Exception as e:
        message = str(e)
        status = 500
    response = make_response({"message": message, "data": result}, status)
    return response
