from datetime import datetime as dt

from config.db import db


class ReviewModel(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=dt.utcnow, nullable=False)

    user = db.relationship("UserModel", backref="reviews")
    article = db.relationship("ArticlesModel", backref="reviews")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)

    __table_args__ = (
        db.CheckConstraint("score >= 0 AND score <= 5", name="check_score_range"),
    )
