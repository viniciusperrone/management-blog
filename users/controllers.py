from flask import request, jsonify
from db import db
from users.models import UserModel
from users.schemas import UserSchema


def create_user():
    data = request.get_json()
    user_schema = UserSchema()

    errors = user_schema.validate(data)

    if errors:
        return jsonify(errors), 400
    
    new_user = UserModel(
        name=data['name'],
        email=data['email'],
        password=data['password']
    )

    existing_user = UserModel.query.filter_by(email=data['email']).first()

    if existing_user:
        return jsonify({"error": "There is already an email"}), 409

    try:
        db.session.add(new_user)
        db.session.commit()

        return jsonify(user_schema.dump(new_user)), 201
    except Exception:
        return jsonify({"message": "Server Internal Error"}), 500
