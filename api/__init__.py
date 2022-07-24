from flask import Blueprint

api = Blueprint('api', __name__)

from . import record_api, standard_api, user_api