from flask import Blueprint

from authentication.controllers import login


authentication_blueprint = Blueprint('authentication', __name__)

authentication_blueprint.add_url_rule('/authentication/login', view_func=login, methods=['POST'])
