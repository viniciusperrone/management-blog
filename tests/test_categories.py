import pytest
from flask import request


def test_create_category(client, auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}" 
    }
    data = {"name": "Technology"}

    response = client.post(
        "/articles/category/new", 
        headers=headers, 
        json=data
    )

    assert response.status_code == 201
    assert response.json["name"] == "Technology"
