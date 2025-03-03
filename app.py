from flask import Flask
from flask_migrate import Migrate
from db import db

import users
import articles
import reviews

from users.routes import users_blueprint
from articles.routes import articles_blueprint
from reviews.routes import reviews_blueprint


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://myuser:mypassword@db/core"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True 

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(users_blueprint)
app.register_blueprint(articles_blueprint)
app.register_blueprint(reviews_blueprint)

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000
    )
