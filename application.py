import os
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

CORS(app)
connect(host=os.environ.get('MONGO_URI'))

if __name__ == '__main__':
    app.run(debug=True)