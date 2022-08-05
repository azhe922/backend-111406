from enums.training_part import TrainingPart
from enums.gender import Gender
from datetime import datetime, timedelta, timezone
from model.record import Record
from model.standard import Standard


def add_record(record_data):
    user_id = record_data['user_id']
    part = TrainingPart(record_data['part'])
    times = record_data['times']
    angles = record_data['angles']
    create_time = datetime.now(timezone(timedelta(hours=+8)))

    record = Record(user_id=user_id, part=part, times=times,
                    angles=angles, create_time=create_time)
    record.save()


def search(user_id, isfirst=False):
    records = []
    results = Record.objects[:1](user_id=user_id).order_by(
        '-create_time') if isfirst else Record.objects(user_id=user_id).order_by('-create_time')
    for record in results:
        record_data = {}
        record_data['_id'] = str(record.id)
        record_data['part'] = record.part.description
        record_data['times'] = record.times
        record_data['angles'] = record.angles
        record_data['create_time'] = record.create_time.strftime(
            "%Y-%m-%d %H:%M:%S")
        records.append(record_data)

    return records


def get_standard_times(data):
    times = []
    age = data['age']
    gender = Gender(data['gender'])
    part = TrainingPart(data['part'])
    for standard in Standard.objects(age__lte__0=age, age__gte__1=age, gender=gender, part=part):
        times = standard.times

    if len(times) == 0:
        raise Exception('occurred some unexpected accident')

    return times
