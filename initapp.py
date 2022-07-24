from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    connect(host=app.config['DB_HOST'])
    CORS(app)

    from api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app