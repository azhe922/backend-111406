from flask import Blueprint, request
from enums.training_part import TrainingPart
from enums.gender import Gender

from service.standard_service import get_times_service

standard_route = Blueprint('standard_route', __name__)
root_path = "/api/standard"

@standard_route.route(f"{root_path}/get/times", methods=['GET'])
def search():
    data = request.get_json()

    return get_times_service(data)
