from marshmallow import Schema, fields

from users.schemas import UserSchema


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=lambda s: len(s) > 5)
 
    created_at = fields.DateTime(dump_only=True)


class ArticleSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    slug = fields.Str(required=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    categories = fields.List(fields.Nested(CategorySchema), dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)
