import os
import pytest

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

