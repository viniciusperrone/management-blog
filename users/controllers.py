from flask import request, jsonify
from flasgger import swag_from
from config.db import db

from users.models import UserModel
from users.schemas import UserSchema


@swag_from({
    'tags': ['User'],
    'summary': 'Create User',
    'description': 'Create User',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'User created successfully'},
        400: {'description': 'Invalid Data'},
        409: {'description': 'There is already an email'},
        500: {'description': 'Internal server error'}
    }
})
def create_user():
    data = request.get_json()
    user_schema = UserSchema()

    errors = user_schema.validate(data)

    if errors:
        return jsonify(errors), 400
    
    new_user = UserModel(
        name=data['name'],
        email=data['email'],
    )
    new_user.set_password(data['password'])

    existing_user = UserModel.query.filter_by(email=data['email']).first()

    if existing_user:
        return jsonify({"error": "There is already an email"}), 409


    try:
        db.session.add(new_user)
        db.session.commit()

        return jsonify(user_schema.dump(new_user)), 201
    except Exception:
        return jsonify({"message": "Internal Server Error"}), 500
