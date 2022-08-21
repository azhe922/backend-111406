from app.model.target import Target
from app.utils.backend_util import dict_to_json


def add_target_service(target_data):
    target_json = dict_to_json(target_data)
    target = Target().from_json(target_json)
    target.save()


def get_target_service(user_id):
    for target in Target.objects(user_id=user_id):
        target_data = target.to_json()['user_todo']
        return target_data
