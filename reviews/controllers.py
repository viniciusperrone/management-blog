from flask import jsonify, request
from db import db
from reviews.models import ReviewModel
from reviews.schema import ReviewSchema
from users.models import UserModel
from articles.models import ArticlesModel


def list_review():
    reviews = ReviewModel.query.all()
    reviews_schema = ReviewSchema(many=True)
    
    return jsonify(reviews_schema.dump(reviews)), 200


def detail_review(review_id):
    review = ReviewModel.query.get(review_id)
    review_schema = ReviewSchema()

    if not review:
        return jsonify({"message": "Review not found"}), 400
    
    return jsonify(review_schema.dump(review)), 200
    

def create_review():
    data = request.get_json()
    review_schema = ReviewSchema()

    errors = review_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    existing_user = UserModel.query.get(data["user_id"])

    if not existing_user:
        return jsonify({"message": "Doesn't match user with given id"})

    existing_article = ArticlesModel.query.get(data["article_id"])

    if not existing_article:
        return jsonify({"message": "Doesn't match article with given id"})

    try:
        new_review = ReviewModel(
            message=data["message"],
            score=data["score"],
            user_id=data["user_id"],
            article_id=data["article_id"]
        )
        
        db.session.add(new_review)
        db.session.commit()

        return jsonify(review_schema.dump(new_review)), 201

    except Exception as e:
        print(str(e))

        return jsonify({"message": "Server Internal Error"}), 500


def delete_review(review_id):
    ...
