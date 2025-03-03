import os
from dotenv import load_dotenv

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from db import db

import users
import articles
import reviews

from users.routes import users_blueprint
from articles.routes import articles_blueprint
from reviews.routes import reviews_blueprint
from authentication.routes import authentication_blueprint


load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SQLALCHEMY_ECHO'] = os.getenv('SQLALCHEMY_ECHO') 
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)

app.register_blueprint(users_blueprint)
app.register_blueprint(articles_blueprint)
app.register_blueprint(reviews_blueprint)
app.register_blueprint(authentication_blueprint)

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000
    )
