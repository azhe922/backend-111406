from flask import Blueprint, g

api = Blueprint('api', __name__)

from . import target_api, log_api, mail_api, record_api, user_api

@api.after_request
def add_header(response):
    token = g.get("token")
    if token:
        response.headers['token'] = token
    return response