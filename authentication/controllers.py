from flask import jsonify, request
from flask_jwt_extended import create_access_token
from flasgger import swag_from

from authentication.schema import AuthenticationSchema
from users.models import UserModel


@swag_from({
    'tags': ['Auth'],
    'summary': 'Login',
    'description': 'JWT Auth',
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
        200: {'description': 'Created Access Token'},
        404: {'description': 'Invalid email or password'},
        500: {'description': 'Internal server error'}
    }
})
def login():
    data = request.get_json()
    authentication_schema = AuthenticationSchema()

    errors = authentication_schema.validate(data)

    if errors:
        return jsonify(errors), 400
    
    email = data["email"]
    password = data["password"]

    user = UserModel.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 404

    try:
        access_token = create_access_token(identity=email)

        return jsonify(access_token=access_token), 200

    except Exception as e:
        print('error', str(e))
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500
