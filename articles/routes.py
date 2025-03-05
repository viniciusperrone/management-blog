from flask import Blueprint

from articles.controllers import (
    create_category, list_categories, create_article,
    list_articles, detail_article, update_article,
    delete_article, search_article
)


articles_blueprint = Blueprint('articles', __name__)

articles_blueprint.add_url_rule('/articles', view_func=list_articles, methods=['GET'])
articles_blueprint.add_url_rule('/articles/search', view_func=search_article, methods=['GET'])
articles_blueprint.add_url_rule('/articles', view_func=create_article, methods=['POST'])

articles_blueprint.add_url_rule('/articles/<int:article_id>/', view_func=detail_article, methods=['GET'])
articles_blueprint.add_url_rule('/articles/<int:article_id>/', view_func=update_article, methods=['PUT'])
articles_blueprint.add_url_rule('/articles/<int:article_id>/', view_func=delete_article, methods=['DELETE'])

articles_blueprint.add_url_rule('/articles/category/list', view_func=list_categories, methods=['GET'])
articles_blueprint.add_url_rule('/articles/category/new', view_func=create_category, methods=['POST'])
