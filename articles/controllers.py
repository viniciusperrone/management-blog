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
        return jsonify({"error": "This category already exists"}), 401


    try:
        db.session.add(new_category)
        db.session.commit()

        return jsonify(category_schema.dump(new_category)), 201

    except Exception:
        return jsonify({"message": "Server Internal Error"}), 500


def list_articles():
    # articles = 
    ...


def detail_article():
    ...

def create_article():
    ...

def update_article():
    ...

def delete_article():
    ...
