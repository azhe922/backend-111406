from flask import Blueprint

api = Blueprint('api', __name__)

from . import mail_api, record_api, standard_api, user_api