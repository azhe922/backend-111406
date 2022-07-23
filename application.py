from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from api.user_api import user_route
from api.record_api import record_route
from api.standard_api import standard_route
import logging
import logging.config
import yaml

app = Flask(__name__)

app.register_blueprint(user_route)
app.register_blueprint(record_route)
app.register_blueprint(standard_route)

app.config.from_object('config.ProductionConfig')
with open(file="./logconfig.yaml", mode='r', encoding="utf-8") as file:
    logging_yaml = yaml.load(stream=file, Loader=yaml.FullLoader)
    logging.config.dictConfig(config=logging_yaml)
CORS(app)
connect(host=app.config['DB_HOST'])

if __name__ == '__main__':
    app.run(threaded=True)