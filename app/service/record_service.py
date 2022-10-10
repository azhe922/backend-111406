from app.enums.training_part import TrainingPart
from app.enums.gender import Gender
from datetime import datetime
from app.model.record import Record
from app.model.standard import Standard
from app.utils.backend_util import dict_to_json
import time


def add_record_service(record_data):
    record_data['create_time'] = int(time.time())
    record_json = dict_to_json(record_data)
    record = Record().from_json(record_json)
    record.save()


def search_record_service(user_id, part, isfirst=False):
    records = []
    results = Record.objects[:1](user_id=user_id, part=part).order_by(
        '-create_time') if isfirst else Record.objects(user_id=user_id).order_by('-create_time')
    for record in results:
        record_data = record.to_json()
        record_data['create_time'] = datetime.fromtimestamp(
            record.create_time).strftime('%Y-%m-%d %H:%M:%S')
        records.append(record_data)

    return records


def get_standard_times_service(data):
    times = []
    age = max(data['age'], 65)
    gender = Gender(data['gender'])
    part = TrainingPart(data['part'])
    for standard in Standard.objects(age__lte__0=age, age__gte__1=age, gender=gender, part=part):
        times = standard.times

    if len(times) == 0:
        raise Exception('occurred some unexpected accident')

    return times
