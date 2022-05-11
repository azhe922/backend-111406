import os
from flask import Flask, jsonify
from flask_cors import CORS
from api.user_api import user_route

app = Flask(__name__)

app.register_blueprint(user_route)


CORS(app)

if __name__ == '__main__':
    app.run(debug=True)


