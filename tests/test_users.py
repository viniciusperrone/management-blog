
import pytest
from flask import json


def test_create_user(client):
    user_data = {
        "name": "Joe Doe",
        "email": "joedoe@gmail.com",
        "password": "master554"
    }

    response = client.post("/users", data=json.dumps(user_data), content_type="application/json")

    assert response.status_code == 201

    response_data = response.get_json()

    assert response_data["name"] == user_data["name"]
    assert response_data["email"] == user_data["email"]
