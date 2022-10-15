from app.model.target import Target
from app.utils.backend_util import dict_to_json, get_week
from datetime import datetime
from app.enums.training_part import TrainingPart


def add_target_service(target_data):
    target_json = dict_to_json(target_data)
    target = Target().from_json(target_json)
    target.save()


def get_target_service(user_id):
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    this_week_days = [d.strftime('%Y%m%d') for d in get_week(now)]
    target = Target.objects(user_id=user_id, end_date__gt=today)
    result = []
    if target:     
        target = target.get()
        user_todos = target.user_todos
        for i in range(len(user_todos)):
            user_todo = user_todos[i]
            target_date = user_todo.target_date
            # 查詢本周所有任務
            if (target_date in this_week_days) and (today >= target_date):
                result.append(user_todo.to_json())
    return result



def update_target_times_service(user_id, target_date, data):
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    target = Target.objects.get(user_id=user_id, end_date__gt=today)
    user_todos = target.user_todos
    for todo_index in range(len(user_todos)):
        user_todo = user_todos[todo_index]
        if user_todo.target_date == target_date:
            actual_times = user_todo.actual_times
            training_part = TrainingPart(data.pop('part')) 

            # 更新實作次數
            match (training_part):
                case TrainingPart.biceps | TrainingPart.deltoid:
                    training_hand = data.pop('hand')
                    actual_times[training_part.value][training_hand] = data
                case TrainingPart.quadriceps:
                    actual_times[training_part.value] = data
            user_todo.actual_times = actual_times

            # 檢查實作次數是否還有比目標次數還小的，沒有的話就代表已完成
            for k in range(3):
                total = user_todo.target_times[k]['total']
                match (k):
                    case 0 | 1:
                        check_complete = [at['times'] for at in [*actual_times[k].values()] if at['times'] < total]
                    case 2:
                        check_complete = True if actual_times[k]['times'] < total else None
                if check_complete:
                    user_todo.complete = False
                    break
                # 這裡可以確定全部的訓練目標都檢查過
                if k == 2:
                    user_todo.complete = True
            
            user_todos[todo_index] = user_todo
            target.update(set__user_todos=user_todos)
            return


def check_target_is_expired(user_id):
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    target = Target.objects(user_id=user_id, end_date__gt=today)
    return True if target else False


def get_target_by_started(user_id):
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    target = Target.objects(user_id=user_id, start_date__gt=today)
    if target:
        return target.get().to_json()