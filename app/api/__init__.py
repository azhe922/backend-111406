from flask import Blueprint, g
from app.utils.backend_util import init_db, close_db

api = Blueprint('api', __name__)

from . import target_api, log_api, mail_api, record_api, user_api

@api.before_request
def before_request():
    init_db()

@api.teardown_request
def teardown_request(exception):
    close_db()

@api.after_request
def after_request(response):
    token = g.get("token")
    if token:
        response.headers['token'] = token
    return response