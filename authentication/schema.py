from marshmallow import Schema, fields


class AuthenticationSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, validate=lambda s: len(s) >= 8)
