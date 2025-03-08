import pytest
import json
from flask import request
from config.db import db

from users.models import UserModel


def test_login_success(client):
    with client.application.app_context():
        user = UserModel(
            name="Joe Doe", 
            email="joedoe@gmail.com",
        )

        user.set_password("master554")

        db.session.add(user)
        db.session.commit()

    login_data = {
        "email": "joedoe@gmail.com",
        "password": "master554"
    }

    response = client.post("/authentication/login", data=json.dumps(login_data), content_type="application/json")

    response_data = response.get_json()

    assert response.status_code == 200

    assert "access_token" in response_data

    assert isinstance(response_data["access_token"], str)

def test_login_invalid_credentials(client):
    login_data = {
        "email": "joedoe2@gmail.com",
        "password": "master123"
    }

    response = client.post("/authentication/login", data=json.dumps(login_data), content_type="application/json")

    response_data = response.get_json()

    assert response.status_code == 404

    assert response_data["message"] == "Invalid email or password"
