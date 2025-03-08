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

    user_response = client.post(
        "/users", 
        json=user_data, 
        content_type="application/json"
    )

    login_response = client.post(
        "/authentication/login", 
        json={"email": user_data["email"], "password": user_data["password"]}
    )

    user_data = json.loads(user_response.data.decode("utf-8"))
    login_data = json.loads(login_response.data.decode("utf-8"))

    auth_response = {
        "user_id": user_data["id"],
        "access_token": login_data["access_token"]
    }

    return auth_response

@pytest.fixture()
def article(client, auth_token):
    access_token = auth_token.get("access_token", "")
    user_id = auth_token.get("user_id", None)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {"name": "Technology"}

    category_response = client.post(
        "/articles/category/new", 
        headers=headers, 
        json=data
    )

    category_data = json.loads(category_response.data.decode("utf-8"))

    article_payload = {
        "title": "Pytest",
        "slug": "pytest",
        "description": "Pytest",
        "user_id": user_id,
        "categories_ids": [category_data["id"]],
    }

    articles_response = client.post(
        "/articles", 
        json=article_payload, 
        headers=headers, 
        content_type="application/json"
    )

    article_data = json.loads(articles_response.data.decode("utf-8"))

    return article_data["id"]
