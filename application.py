from flask import Flask
from flask_cors import CORS
from mongoengine import connect
from api.user_api import user_route
from api.record_api import record_route
from api.standard_api import standard_route

app = Flask(__name__)

app.register_blueprint(user_route)
app.register_blueprint(record_route)
app.register_blueprint(standard_route)

app.config.from_object('config.ProductionConfig')
CORS(app)
connect(host=app.config['DB_HOST'])

if __name__ == '__main__':
    app.run(threaded=True)