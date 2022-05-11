import os
from flask import Flask, jsonify
from flask_cors import CORS
from mongoengine import connect
from api.user_api import user_route

app = Flask(__name__)

app.register_blueprint(user_route)


CORS(app)
connect(host=os.environ.get('MONGO_URI'))

if __name__ == '__main__':
    app.run(debug=True)


