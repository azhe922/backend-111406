from app.enums.training_part import TrainingPart
from app.enums.gender import Gender
from datetime import datetime
from app.model.record import Record
from app.model.standard import Standard
import time


    user_id = record_data['user_id']
    part = TrainingPart(record_data['part'])
    times = record_data['times']
    angles = record_data['angles']
    create_time = int(time.time())

    record = Record(user_id=user_id, part=part, times=times,
                    angles=angles, create_time=create_time)
def add_record_service(record_data):
    record.save()


def search_record_service(user_id, isfirst=False):
    records = []
    results = Record.objects[:1](user_id=user_id).order_by(
        '-create_time') if isfirst else Record.objects(user_id=user_id).order_by('-create_time')
    for record in results:
        record_data = {}
        record_data['_id'] = str(record.id)
        record_data['part'] = record.part.description
        record_data['times'] = record.times
        record_data['angles'] = record.angles
        record_data['create_time'] = datetime.fromtimestamp(
            record.create_time).strftime('%Y-%m-%d %H:%M:%S')
        records.append(record_data)

    return records


def get_standard_times_service(data):
    times = []
    age = data['age']
    gender = Gender(data['gender'])
    part = TrainingPart(data['part'])
    for standard in Standard.objects(age__lte__0=age, age__gte__1=age, gender=gender, part=part):
        times = standard.times

    if len(times) == 0:
        raise Exception('occurred some unexpected accident')

    return times
