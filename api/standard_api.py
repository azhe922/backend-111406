from flask import Blueprint, make_response, request
from service.record_service import search_service

from service.standard_service import get_times_service

standard_route = Blueprint('standard_route', __name__)
root_path = "/api/standard"


@standard_route.route(f"{root_path}/analyze", methods=['POST'])
def analyze_record():
    # the parameter which is like (user_id, age, part, gender, times)
    data = request.get_json()
    message = ""
    status = 200
    result = {}
    try:
        standard = get_times_service(data)
        record = search_service(data['user_id'], True)
        times = data['times']
        compare = [s for s in standard if times >= s]
        difference = times - record[0]['times'] if len(record) > 0 else -999
        pr = len(compare) * 5
        test_result = ""
        if pr > 75:
            test_result = "很棒"
        elif pr > 20:
            test_result = "正常"
        else:
            test_result = "待加強"

        result = {
            "times": times,
            "pr": pr,
            "test_result": test_result
        }
        if difference > -100:
            result["difference"] = difference
        message = "查詢成功"
    except Exception as e:
        message = str(e)
        result = {}
        status = 500
    response = make_response({"message": message, "data": result}, status)
    return response
