from flask import jsonify
from reviews.models import ReviewModel
from reviews.schema import ReviewSchema


def list_review():
    reviews = ReviewModel.query.all()
    reviews_schema = ReviewSchema(many=True)
    
    return jsonify(reviews_schema.dump(reviews)), 200

def detail_review(review_id):
    ...

def create_review():
    ...

def delete_review(review_id):
    ...
