from app.utils.backend_util import dict_to_json, get_now_timestamp
from app.model.logrecord import LogRecord

def add_log_service(log_data):
    log_data['action_time'] = get_now_timestamp()
    log_json = dict_to_json(log_data)
    log = LogRecord().from_json(log_json)
    log.save()