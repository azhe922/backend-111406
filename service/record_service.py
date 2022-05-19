from enums.training_part import TrainingPart
from flask import make_response
from datetime import datetime, timedelta, timezone
from model.record import Record

def add_record_service(record_data):
    try:
        user_id = record_data['user_id']
        part = TrainingPart(record_data['part'])
        type = record_data['type']
        times = record_data['times']
        angles = record_data['angles']
        create_time = datetime.now(timezone(timedelta(hours=+8)))

        record = Record(user_id=user_id, part=part, type=type,
                        times=times, angles=angles, create_time=create_time)
        record.save()

        return make_response({'message': 'succesfully inserted'}, 201)

def search_service(user_id):
    records = []
    try:
        for record in Record.objects(user_id = user_id):
            record_data = {}
            record_data['_id'] = str(record.id)
            record_data['part'] = record.part.description
            record_data['type'] = record.type.description
            record_data['times'] = record.times
            record_data['angles'] = record.angles
            record_data['create_time'] = record.create_time
            records.append(record_data)

        return make_response({'message': '查詢成功', 'data': records}, 200)

    except Exception as e:
        return make_response({'message': str(e)}, 500)
