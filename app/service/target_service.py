from app.model.target import Target
from app.model.target_usertodo import UserTodo
from app.utils.backend_util import dict_to_json, get_week, get_now_timestamp
from datetime import datetime
from app.enums.training_part import TrainingPart
from app.utils.backend_error import UserTodoHasAlreadyCreateException


def add_target_service(target_data):
    target_json = dict_to_json(target_data)
    target = Target().from_json(target_json)
    target.create_time = get_now_timestamp()
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
        for user_todo in user_todos:
            target_date = user_todo.target_date
            # 查詢本周所有任務
            if (target_date in this_week_days) and (today >= target_date):
                result.append(user_todo.to_json())
    return result



def update_target_times_and_return(user_id, target_date, data):
    """
    :param str | None hand: training hand
    :param int part: training part
    :param int times: training times
    :param int fails: fail times
    :param int spending_time: all spend time for training
    """
    target = __get_target_from_today(user_id).get()
    should_be_updated_todo = target.user_todos.filter(target_date=target_date).get()
    updated_actual_times =  __reset_actual_times_and_return(should_be_updated_todo.actual_times, data)         
    should_be_updated_todo.actual_times = updated_actual_times
    __check_target_is_completed(should_be_updated_todo, updated_actual_times)
    target.save()
    return should_be_updated_todo.to_json()


def check_target_existed_service(user_id):
    target = __get_target_from_today(user_id)
    return True if target else False


def check_target_isjuststarted_service(user_id):
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    target = Target.objects(user_id=user_id, start_date__gt=today)
    return True if target else False

def add_todo_service(user_id, todo_data):
    usertodo_json = dict_to_json(todo_data)
    to_add_usertodo = UserTodo.from_json(usertodo_json)

    target = __get_target_from_today(user_id).get()
    user_todos = target.user_todos
    check_istarget_existed = [user_todo for user_todo in user_todos if user_todo.target_date == to_add_usertodo.target_date]
    if check_istarget_existed:
        raise UserTodoHasAlreadyCreateException()
    else:
        target.user_todos.append(to_add_usertodo)
        target.save()

def get_last_and_iscompleted_target(user_id):
    now = get_now_timestamp()
    target = Target.objects(user_id=user_id, create_time__lt=now).order_by('-create_time').first()
    return target.create_time if target else 0


def __get_target_from_today(user_id):
    now = datetime.now()
    today = now.strftime('%Y%m%d')
    return Target.objects(user_id=user_id, end_date__gt=today)

def __reset_actual_times_and_return(actual_times, data):
    to_update_training_part = TrainingPart(data.pop('part'))
    to_update_training_hand = data.pop('hand') if 'hand' in data else None
    to_update_index = __iterate_to_get_updated_index(actual_times, to_update_training_part, to_update_training_hand)
    actual_times[to_update_index]['times'] = data['times']
    actual_times[to_update_index]['spending_time'] = data['spending_time']
    actual_times[to_update_index]['fails'] = data['fails']

    now = get_now_timestamp()
    actual_times[to_update_index]['complete_time'] = now

    return actual_times

def __check_target_is_completed(user_todo, actual_times):
    check_complete = []
    for actual_time in actual_times:
        part = TrainingPart(actual_time['part'])
        total = [filtered_by_part['total'] for filtered_by_part in user_todo.target_times if filtered_by_part.get('part') == part.value][0]
        check_complete.append(True if actual_time['times'] >= total else False)
    user_todo.complete = False if False in check_complete else True


def __iterate_to_get_updated_index(actual_times, to_update_training_part, to_update_training_hand):
    for index in range(len(actual_times)):
        if actual_times[index]['part'] == to_update_training_part.value:
            match to_update_training_part:
                case TrainingPart.biceps | TrainingPart.deltoid:
                    if actual_times[index]['hand'] == to_update_training_hand:
                        return index
                case TrainingPart.quadriceps:
                    return index