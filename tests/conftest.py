import os
import pytest
import json

from app import initialize_app
from config.db import db

import users
import articles
import reviews


os.environ["TESTING"] = "True"

@pytest.fixture()
def app():
    app = initialize_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": True
    })

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth_token(client):
    user_data = {
        "name": "Joe Doe", 
        "email": "joedoe@gmail.com", 
        "password": "master554"
    }

    client.post(
        "/users", 
        json=user_data, 
        content_type="application/json"
    )

    login_response = client.post(
        "/authentication/login", 
        json={"email": user_data["email"], "password": user_data["password"]}
    )

    login_data = json.loads(login_response.data.decode("utf-8"))
    
    return login_data["access_token"]
