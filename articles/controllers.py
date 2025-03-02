from flask import jsonify, request
from db import db

from articles.models import ArticlesModel, CategoryModel
from articles.schemas import ArticleSchema, CategorySchema


def create_category():
    data = request.get_json()

    category_schema = CategorySchema()

    errors = category_schema.validate(data)

    if errors:
        jsonify(errors), 401

    new_category = CategoryModel(
        name=data["name"]
    )

    already_category = CategoryModel.query.filter_by(name=data["name"]).first()

    if already_category:
        return jsonify({"error": "This category already exists"}), 400

    try:
        db.session.add(new_category)
        db.session.commit()

        return jsonify(category_schema.dump(new_category)), 201

    except Exception:
        return jsonify({"message": "Server Internal Error"}), 500


def list_categories():
    categories = CategoryModel.query.all()
    categories_schema = CategorySchema(many=True)

    return jsonify(categories_schema.dump(categories)), 200


def list_articles():
    articles = ArticlesModel.query.all()
    articles_schema = ArticleSchema(many=True)

    return jsonify(articles_schema.dump(articles)), 200

def detail_article(article_id):
    article = ArticlesModel.query.filter_by(id=article_id).first()
    article_schema = ArticleSchema()

    if article is None:
        return jsonify({'message': 'Article not found'}), 400
    
    return jsonify(article_schema.dump(article)), 200


def create_article():
    data = request.get_json()
    article_schema = ArticleSchema()

    errors = article_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    already_existing_slug = ArticlesModel.query.filter_by(slug=data["slug"]).first()

    if already_existing_slug:
        return jsonify({'message': 'Slug already exist'}), 400
    
    try:
        new_article = ArticlesModel(data=data)

        db.session.add(new_article)
        db.session.commit()

        return jsonify(article_schema.dump(data))
    except Exception:
        return jsonify({"message": "Server Internal Error"}), 500


def update_article(article_id):
    data = request.get_json()
    article_schema = ArticleSchema(partial=True)
    article = ArticlesModel.query.get(id=article_id)

    if not article:
        return jsonify({"error": "Article not found"}), 404

    errors = article_schema.validate(data)

    if errors:
        return jsonify(errors), 400
    
    already_existing_slug = ArticlesModel.query.filter(
        ArticlesModel.slug == data.get("slug"), ArticlesModel.id != article_id
    ).first()

    if already_existing_slug:
        return jsonify({'message': 'Slug already exist'}), 400
    
    try:
        for key, value in data.items():
            setattr(article, key, value)

        db.session.commit()

        return jsonify(article_schema.dump(article)), 200
    except Exception:
        return jsonify({"message": "Server Internal Error"}), 500

def delete_article(article_id):
    article = ArticlesModel.query.get(id=article_id)

    if not article:
        return jsonify({"error": "Article not found"}), 404

    db.session.delete(article)
    db.session.commit()

    return jsonify({"message": "Article deleted successfully"}), 201
