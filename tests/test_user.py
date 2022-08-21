from app.service.user_service import user_signup, update_user
from app.model.user import User
import json
import logging

LOGGER = logging.getLogger(__name__)

def test_index(client):
    data = {
        "user_id": "aaaaaa",
        "password":"sdadsadasd"
    }
    data = str(data).replace("\'", "\"")
    # response = client.post("/api/user/login", data=data, headers={'Content-Type': 'application/json; charset=utf-8'})
    
    # print(response.data.decode('utf-8'))

# def test_signup(client):
#     user_json = User(user_id="aaaaaa", 
#     password = "sdadsadasd",
#     email = "zsda5858sda@gmail",
#     gender = 0,
#     birthday = "19550101",
#     role = "N").to_json()
#     print(user_json)
#     response = client.post("api/user/signup", data=user_json)
#     print(response)


def test_update(client):
    user_json = User(user_id="aaaaaa", 
    password = "sdadsadasd",
    email = "zsda5858sda@gmail",
    gender = 0,
    birthday = "19550101",
    role = "N").to_json()
    print(json.dumps(user_json))
    # response = client.post("api/user/update", data=user_json)
    # print(response)
