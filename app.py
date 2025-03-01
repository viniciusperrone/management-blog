from flask import Flask
from db import db


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://myuser:mypassword@db/core"

db.init_app(app)

if __name__ == "__main__":
  app.run(
      host="127.0.0.1",
      port=5000
  )
