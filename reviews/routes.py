from flask import Blueprint

from reviews.controllers import list_review, detail_review, create_review, delete_review


reviews_blueprint = Blueprint('reviews', __name__)

reviews_blueprint.add_url_rule('/reviews', view_func=list_review, methods=['GET'])
reviews_blueprint.add_url_rule('/reviews', view_func=create_review, methods=['POST'])

reviews_blueprint.add_url_rule('/articles/<int:article_id>/', view_func=detail_review, methods=['GET'])
reviews_blueprint.add_url_rule('/articles/<int:article_id>/', view_func=delete_review, methods=['DELETE'])
