from flask import Flask
from flask_migrate import Migrate
from db import db
import users


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://myuser:mypassword@db/core"

db.init_app(app)

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000
    )
