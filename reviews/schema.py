from marshmallow import Schema, fields


class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    message = fields.Str(required=True)
    score = fields.Float(nullable=True, validate=lambda s: s >= 0 and s <= 5)
    created_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(require=True)
    article_id = fields.Int(require=True)
