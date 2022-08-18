from app.service.user_service import signup
from app.model.user import User
import json
import logging

LOGGER = logging.getLogger(__name__)

def test_index(client):
    data = {
        "user_id": "zsda5858sda",
        "password":"sdasda5654"
    }

    # response = client.post("http://localhost:5000/api/user/login", data=json.dumps(data))
    
    # print(response)
    # assert len(response.data) > 0

def test_signup(client):
    user_json = User(user_id="aaaaaa", 
    password = "sdadsadasd",
    email = "zsda5858sda@gmail",
    gender = 0,
    birthday = "19550101",
    role = "N").to_json()
    print(user_json)
    response = client.post("api/user/signup", data=user_json)
    print(response)
