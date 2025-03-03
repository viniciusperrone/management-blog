from flask import jsonify, request
from flask_jwt_extended import create_access_token

from authentication.schema import AuthenticationSchema
from users.models import UserModel

def login():
    data = request.get_json()
    authentication_schema = AuthenticationSchema()

    errors = authentication_schema.validate(data)

    if errors:
        return jsonify(errors), 400
    
    email = data["email"]
    password = data["password"]

    UserModel.query.filter_by(email=email, password=password).first_or_404("Invalid email or password")

    access_token = create_access_token(identity=email)

    return jsonify(access_token=access_token), 200
