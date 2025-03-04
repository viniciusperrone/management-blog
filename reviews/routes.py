from flask import Blueprint

from reviews.controllers import list_review, detail_review, create_review, delete_review, get_reviews_by_article


reviews_blueprint = Blueprint('reviews', __name__)

reviews_blueprint.add_url_rule('/reviews', view_func=list_review, methods=['GET'])
reviews_blueprint.add_url_rule('/reviews', view_func=create_review, methods=['POST'])

reviews_blueprint.add_url_rule('/reviews/<int:review_id>/', view_func=detail_review, methods=['GET'])
reviews_blueprint.add_url_rule('/reviews/<int:review_id>/', view_func=delete_review, methods=['DELETE'])

reviews_blueprint.add_url_rule(
  '/article/reviews/<int:article_id>/', 
  view_func=get_reviews_by_article, 
  methods=['GET'], 
)
