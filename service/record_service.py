from enums.training_part import TrainingPart
from datetime import datetime, timedelta, timezone
from model.record import Record


def add_record_service(record_data):
    user_id = record_data['user_id']
    part = TrainingPart(record_data['part'])
    type = record_data['type']
    times = record_data['times']
    angles = record_data['angles']
    create_time = datetime.now(timezone(timedelta(hours=+8)))

    record = Record(user_id=user_id, part=part, type=type,
                    times=times, angles=angles, create_time=create_time)
    record.save()


def search_service(user_id, isfirst=False):
    records = []
    results = Record.objects[:1](user_id=user_id).order_by(
        '-create_time') if isfirst else Record.objects(user_id=user_id).order_by('-create_time')
    for record in results:
        record_data = {}
        record_data['_id'] = str(record.id)
        record_data['part'] = record.part.description
        record_data['type'] = record.type.description
        record_data['times'] = record.times
        record_data['angles'] = record.angles
        record_data['create_time'] = record.create_time.strftime("%Y-%m-%d %H:%M:%S")
        records.append(record_data)
    
    return records
