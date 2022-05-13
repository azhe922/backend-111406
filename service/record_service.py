from model.record import Record
from flask import make_response
import datetime

def add_record_service(record_data):
    try:
        user_id = record_data['user_id']
        part = record_data['part']
        type = record_data['type']
        times = record_data['times']
        angles = record_data['angles']
        create_time = datetime.datetime.now()

        record = Record(user_id=user_id, part=part, type=type,
                          times=times, angles=angles, create_time=create_time)
        record.save()

        return make_response({'message' : 'succesfully inserted'}, 201)        
    except Exception as e:
        return make_response({'message' : str(e)}, 404)  

