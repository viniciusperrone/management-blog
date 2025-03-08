import pytest
from flask import request


def test_create_category(client, auth_token):
    access_token = auth_token.get("access_token", "")
    
    headers = {
        "Authorization": f"Bearer {access_token}" 
    }
    data = {"name": "Technology"}

    response = client.post(
        "/articles/category/new", 
        headers=headers, 
        json=data
    )

    assert response.status_code == 201
    assert response.json["name"] == "Technology"
