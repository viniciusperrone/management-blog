from flask import jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from config.elasticsearch_client import es
from db import db

from articles.models import ArticlesModel, CategoryModel
from articles.schemas import ArticleSchema, CategorySchema
from users.models import UserModel
from users.schemas import UserSchema


@jwt_required()
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


@jwt_required()
def list_categories():
    categories = CategoryModel.query.all()
    categories_schema = CategorySchema(many=True)

    return jsonify(categories_schema.dump(categories)), 200


@jwt_required()
def list_articles():
    page = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('per_page', 10, type=int)

    pagination_articles = ArticlesModel.query.paginate(
        page=page,
        per_page=items_per_page,
        error_out=False
    )

    articles = pagination_articles.items

    articles_schema = ArticleSchema(many=True)

    return jsonify({
        "total": pagination_articles.total,
        "page": pagination_articles.page,
        "per_page": pagination_articles.per_page,
        "pages": pagination_articles.page,
        "has_next": pagination_articles.has_next,
        "has_prev": pagination_articles.has_prev,
        "articles": articles_schema.dump(articles)
    }), 200

@jwt_required()
def detail_article(article_id):
    article = ArticlesModel.query.get(article_id)
    article_schema = ArticleSchema()

    if article is None:
        return jsonify({'message': 'Article not found'}), 400
    
    return jsonify(article_schema.dump(article)), 200


@jwt_required()
def create_article():
    data = request.get_json()
    article_schema = ArticleSchema()
    user_schema = UserSchema(only=["name", "email"])

    errors = article_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    already_existing_slug = ArticlesModel.query.filter_by(slug=data["slug"]).first()

    if already_existing_slug:
        return jsonify({'message': 'Slug already exist'}), 400
    
    categories = []
    category_ids = data.get("categories_ids", [])

    if not category_ids:
        return jsonify({"message": "At least one category is required"}), 400

    for category_id in category_ids:
        category = CategoryModel.query.get(category_id)

        if not category:
            return jsonify({"message": f"Doesn't match category with given id {category_id}"}), 400

        categories.append(category)       

    data["categories"] = categories

    existing_user = UserModel.query.get(data.get("user_id"))

    if not existing_user:
        return jsonify({"message": "Doesn't match user with given id"})

    data["user"] = existing_user

    try:
        new_article = ArticlesModel(
            title=data["title"],
            slug=data["slug"],
            description=data["description"],
            user=existing_user,
            categories=categories
        )

        db.session.add(new_article)

        db.session.commit()

        es.index(
            index="articles", 
            id=new_article.id,
            body={
                "title": new_article.title,
                "description": new_article.description,
                "slug": new_article.slug,
                "user": user_schema.dump(existing_user),
                "categories": [category.name for category in new_article.categories],
            }
        )


        return jsonify(article_schema.dump(data))
    except SQLAlchemyError as e:
        db.session.rollback()

        return jsonify({"message": "Database Error", "error": str(e)}), 500
    except Exception as e:
        db.session.rollback()

        return jsonify({"message": "Server Internal Error", "error": str(e)}), 500


@jwt_required()
def update_article(article_id):
    data = request.get_json()
    article_schema = ArticleSchema(partial=True, exclude=["user_id"])
    article = ArticlesModel.query.get(article_id)

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
    
    category_ids = data.get("categories_ids", [])

    if category_ids:
        categories = []

        for category_id in category_ids:
            category = CategoryModel.query.get(category_id)

            if not category:
                return jsonify({"message": f"Doesn't match category with given id {category_id}"}), 400

            categories.append(category)       

        data["categories"] = categories

        data.pop("categories_ids")

    try:
        for key, value in data.items():
            setattr(article, key, value)

        db.session.commit()

        return jsonify(article_schema.dump(article)), 200
    except Exception:
        return jsonify({"message": "Server Internal Error"}), 500


@jwt_required()
def delete_article(article_id):
    article = ArticlesModel.query.get(article_id)

    if not article:
        return jsonify({"error": "Article not found"}), 404

    try:
        es.delete(index="articles", id=article_id)

        db.session.delete(article)

        db.session.commit()

        return jsonify({"message": "Article deleted successfully"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()

        return jsonify({"message": "Database Error", "error": str(e)}), 500
    except Exception as e:
        db.session.rollback()

        return jsonify({"message": "Server Internal Error", "error": str(e)}), 500


@jwt_required()
def search_article():
    query = request.args.get("query", "")

    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "description", "user.name", "user.email", "categories"]
            }
        }
    }

    results = es.search(index="articles", body=search_body)

    articles = [
        {**hit["_source"]}
        for hit in results["hits"]["hits"]
    ]

    return jsonify(articles), 200
