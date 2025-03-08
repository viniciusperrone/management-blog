import pytest
from flask import request

from config.db import db
from articles.models import CategoryModel


def test_create_article(client, auth_token):
    user_id = auth_token.get("user_id", None)
    access_token = auth_token.get("access_token", "")
    
    headers = {
        "Authorization": f"Bearer {access_token}" 
    }

    category_data = {
        "name": "pytest"
    }

    with client.application.app_context():
        category = CategoryModel(
            name=category_data["name"],
        )

        db.session.add(category)
        db.session.commit()

        db.session.refresh(category)

    article_data = {
        "title": "Pytest",
        "slug": "pytest",
        "description": "Pytest",
        "user_id": user_id,
        "categories_ids": [category.id],
    }

    articles_response = client.post(
        "/articles", 
        json=article_data, 
        headers=headers, 
        content_type="application/json"
    )

    assert articles_response.status_code == 201

def test_get_article(client, auth_token, article):
    access_token = auth_token.get("access_token", "")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get(f"/articles/{article}/", headers=headers)

    assert response.status_code == 200
    assert response.json["id"] == article

def test_update_article(client, auth_token, article):
    access_token = auth_token.get("access_token", "")
    headers = {"Authorization": f"Bearer {access_token}"}

    updated_article_data = {
        "title": "Updated Title",
        "slug": "updated-title",
        "description": "updated description",
    }

    response = client.put(
        f"/articles/{article}/", 
        json=updated_article_data, 
        headers=headers
    )

    assert response.status_code == 200

def test_delete_article(client, auth_token, article):
    access_token = auth_token.get("access_token", "")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.delete(f"/articles/{article}/", headers=headers)

    assert response.status_code == 201
