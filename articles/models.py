from config.db import db, articles_categories

from datetime import datetime


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    articles = db.relationship("ArticlesModel", secondary=articles_categories, back_populates="categories")

class ArticlesModel(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    user = db.relationship("UserModel", backref="articles")
    categories = db.relationship("CategoryModel", secondary=articles_categories, back_populates="articles")
