from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from mongoengine import connect
from app_config import config
from dotenv import load_dotenv

mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    connect(host=app.config['DB_HOST'])
    CORS(app)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app