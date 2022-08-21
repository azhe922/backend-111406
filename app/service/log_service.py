from app.utils.backend_util import dict_to_json
from datetime import datetime
from app.model.logrecord import LogRecord
import time

def add_log_service(log_data):
    log_data['action_time'] = int(time.time())
    log_json = dict_to_json(log_data)
    log = LogRecord().from_json(log_json)
    log.save()

def search_log_service(start_time, end_time):
    logs = []
    for log in LogRecord.objects(action_time__gte=start_time, action_time__lte = end_time).order_by('-action_time'):
        log_data = log.to_json()
        log_data['action_time'] = datetime.fromtimestamp(
            log.action_time).strftime('%Y-%m-%d %H:%M:%S')
        logs.append(log_data)

    return logs