from app.model.target import Target
from app.utils.backend_util import dict_to_json
from app.model.target_usertodo import UserTodo


def add_target_service(target_data):
    target_json = dict_to_json(target_data)
    target = Target().from_json(target_json)
    target.save()


def get_target_service(user_id):
    for target in Target.objects(user_id=user_id):
        target_data = target.to_json()['user_todo']
        return target_data


def update_target_times_service(user_id, target_date, data):
    for target in Target.objects(user_id=user_id).only("user_todos"):
        user_todos = target.user_todos
        for i in range(len(user_todos)):
            user_todo = user_todos[i]
            if user_todo.target_date == target_date:
                actual_times = user_todo.actual_times
                training_part = data['part']
                data.pop('part', None)
                # 更新實作次數
                user_todo.actual_times = [actual_times[k] if k !=
                                          training_part else data for k in range(len(actual_times))]

                # 檢查實作次數是否還有比目標次數還小的，沒有的話就代表已完成
                check_complete = [i for i in range(
                    3) if user_todo.actual_times[i]['times'] < user_todo.target_times[i]['total']]
                user_todo.complete = True if not check_complete else False
                user_todos[i] = user_todo
                target.update(set__user_todos=user_todos)
                return
