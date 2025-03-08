from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from config.db import db

from reviews.models import ReviewModel
from reviews.schema import ReviewSchema
from users.models import UserModel
from articles.models import ArticlesModel


@swag_from({
    'tags': ['Review'],
    'summary': 'List Review',
    'description': 'List All Review',
    'responses': {
        200: {'description': 'List all successful reviews'},
        401: {'description': 'Missing Token'},
        500: {'description': 'Internal server error'}
    }
})
@jwt_required()
def list_review():
    reviews = ReviewModel.query.all()
    reviews_schema = ReviewSchema(many=True)
    
    return jsonify(reviews_schema.dump(reviews)), 200


@swag_from({
    'tags': ['Review'],
    'summary': 'Detail Review',
    'description': 'Detail Review',
    'parameters': [
        {'name': 'review_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Review ID'}
    ],
    'responses': {
        200: {'description': 'Review found successfully'},
        401: {'description': 'Missing Token'},
        404: {'description': 'Review not found'},
        500: {'description': 'Internal server error'}
    }
})
@jwt_required()
def detail_review(review_id):
    review = ReviewModel.query.get(review_id)
    review_schema = ReviewSchema()

    if not review:
        return jsonify({"message": "Review not found"}), 404
    
    return jsonify(review_schema.dump(review)), 200


@swag_from({
    'tags': ['Review'],
    'summary': 'Get Reviews By Article',
    'description': 'Reviews By Article',
    'parameters': [
        {'name': 'article_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Review ID'}
    ],
    'responses': {
        200: {'description': 'Reviews found successfully'},
        401: {'description': 'Missing Token'},
        500: {'description': 'Internal server error'}
    }
})
@jwt_required()
def get_reviews_by_article(article_id):
    reviews = ReviewModel.query.filter_by(article_id=article_id)
    reviews_schema = ReviewSchema(many=True)

    return jsonify(reviews_schema.dump(reviews)), 200
    

@swag_from({
    'tags': ['Review'],
    'summary': 'Create a new review',
    'description': 'Create review by article',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer'},
                    'article_id': {'type': 'integer'},
                    'message': {'type': 'string'},
                    'score': {'type': 'number'},
                },
                'required': ['user_id', 'article_id', 'message']
            }
        }
    ],
    'responses': {
        201: {'description': 'Review created successfully'},
        401: {'description': 'Invalid Data'},
        401: {'description': 'Invalid Token'},
        404: {'description': 'Not Found User or Article given ids'},
        500: {'description': 'Internal server error'}
    }
})
@jwt_required()
def create_review():
    data = request.get_json()
    review_schema = ReviewSchema()

    errors = review_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    existing_user = UserModel.query.get(data["user_id"])

    if not existing_user:
        return jsonify({"message": "Doesn't match user with given id"}), 404

    existing_article = ArticlesModel.query.get(data["article_id"])

    if not existing_article:
        return jsonify({"message": "Doesn't match article with given id"}), 404

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

        return jsonify({"message": "Internal Server Error"}), 500


@swag_from({
    'tags': ['Review'],
    'summary': 'Delete Review',
    'description': 'Delete Review',
    'parameters': [
        {'name': 'review_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Review ID'}
    ],
    'responses': {
        201: {'description': 'Review deleted successfully'},
        401: {'description': 'Missing Token'},
        500: {'description': 'Internal server error'}
    }
})
@jwt_required()
def delete_review(review_id):
    review = ReviewModel.query.get(review_id)

    if not review:
        return jsonify({"error": "Review not found"}), 404

    try:
        db.session.delete(review)
        db.session.commit()

        return jsonify({"message": "Review deleted successfully"}), 201

    except Exception:
        return jsonify({"message": "Internal Server Error"}), 500
