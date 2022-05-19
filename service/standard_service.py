from flask import make_response
from enums.gender import Gender
from enums.training_part import TrainingPart

from model.standard import Standard


def get_times_service(data):
    times = []
    try:
        age = data['age']
        gender = Gender(data['gender'])
        part = TrainingPart(data['part'])
        for standard in Standard.objects(age__lte__0=age, age__gte__1=age, gender=gender, part=part):
            times = standard.times
        
        if len(times) == 0: raise Exception('occurred some unexpected accident')

        return make_response({'message': '查詢成功', 'data': times}, 200)

    except Exception as e:
        return make_response({'message': str(e)}, 500)
