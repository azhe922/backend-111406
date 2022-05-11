import os
from flask import Flask, jsonify
from api.user_api import user_route

app = Flask(__name__)

app.register_blueprint(user_route)



if __name__ == '__main__':
    app.run(debug=True)


