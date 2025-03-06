import pytest
import json
from flask import request
from db import db

from users.models import UserModel


def test_login_success(client):
    user = UserModel(name="Joe Doe", email="joedoe@gmail.com", password="master554")
    db.session.add(user)
    db.session.commit()

    login_data = {
        "email": "joedoe@gmail.com",
        "password": "master554"
    }

    response = client.post("/authentication/login", data=json.dumps(login_data), content_type="application/json")

    assert response.status_code == 200

    response_data = response.get_json()

    assert "access_token" in response_data
    assert isinstance(response_data["access_token"], str)
