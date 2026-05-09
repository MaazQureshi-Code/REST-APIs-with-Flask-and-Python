import os
import uuid
from flask import Flask
from flask_smorest import Api
from resources.item import bip as ItemBlueprint
from resources.store import bip as StoreBlueprint
from resources.tag import bip as TagBlueprint
from db import db
import models
def create_app(db_url=None):
     app = Flask(__name__)
     app.config["API_TITLE"] = "Stores API"
     app.config["API_VERSION"] = "v1"
     app.config["OPENAPI_VERSION"] = "3.0.3"
     app.config["PROPAGATE_EXCEPTIONS"] = True
     app.config["OPENAPI_URL_PREFIX"] = "/"
     app.config["OPENAPI_JSON_PATH"] = "openapi.json"
     app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
     app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
     app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL") or "sqlite:///data.db"
     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
     db.init_app(app)
     
     api = Api(app)
     @app.before_first_request
     def create_tables():
          db.create_all()
     api.register_blueprint(ItemBlueprint)
     api.register_blueprint(StoreBlueprint)
     api.register_blueprint(TagBlueprint)
     
     return app
