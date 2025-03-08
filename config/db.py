from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

articles_categories = db.Table(
    "articles_categories",
    db.Column("article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True),
    db.Column("category_id", db.Integer, db.ForeignKey("categories.id"), primary_key=True),
)
