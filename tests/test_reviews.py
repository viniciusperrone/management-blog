import pytest
from flask import request

from config.db import db
from reviews.models import ReviewModel


def test_create_review(client, auth_token, article):
    access_token = auth_token.get("access_token", "")
    user_id = auth_token.get("user_id", None)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    review_payload = {
        "message": "Message Test",
        "score": 5.0,
        "user_id": user_id,
        "article_id": article
    }

    response = client.post("/reviews", json=review_payload, headers=headers)

    assert response.status_code == 201

def test_delete_review(client, auth_token, article):
    access_token = auth_token.get("access_token", "")
    user_id = auth_token.get("user_id", None)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    with client.application.app_context():
        new_review = ReviewModel(
            message="Message Test",
            score=5.0,
            user_id=user_id,
            article_id=article
        )

        db.session.add(new_review)
        db.session.commit()

        db.session.refresh(new_review)

    response = client.delete(f"/reviews/{new_review.id}/", headers=headers)

    assert response.status_code == 201
