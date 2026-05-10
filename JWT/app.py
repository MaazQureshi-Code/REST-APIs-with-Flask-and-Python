from flask import Flask ,jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
import models
import secrets
from db import db
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST
def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    app.config["JWT_SECRET_KEY"] = secrets.token_hex(16)  # Change this in a real app!
    jwt = JWTManager(app)
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            {"message": "The token has expired.", "error": "token_expired"},
            401,
        )
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            {"message": "Signature verification failed.", "error": "invalid_token"},
            401,
        )
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            {"message": "Request does not contain an access token.", "error": "authorization_required"},
            401,
        )
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            {"message": "Request does not contain an access token.", "error": "authorization_required"},
            401,
        )
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            {"message": "The token has been revoked.", "error": "token_revoked"},
            401,
        )
    
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
