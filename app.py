from blocklist import BLOCKLIST
from flask import Flask, jsonify, g
from flask_smorest import Api
from flask_migrate import Migrate
import database.config.db as db
import os
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.user import blp as UserBlueprint
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import newrelic.agent
from contextlib import contextmanager

CURRENT_ENV = os.getenv("ENVIRONMENT", "local")
newrelic.agent.initialize('newrelic.ini', environment=CURRENT_ENV)

def create_app(db_url=None) -> Flask:
    db_session = db.db_start()

    def get_db_session():
        return db_session
    
    app = Flask(__name__)
    load_dotenv()
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    #app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    #app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "secret_key"

    # Used when connecting app to `from flask_sqlalchemy import SQLAlchemy` object
    # db_instance.init_app(app)

    #using flask_migrate to handle db upgrade
    #using this requires to remove sql alchemy code to generate tables in line 83-84
    #run to create migration and basic files
    #flask db init
    #run to generate the first upgrade script and empty
    #flask db migrate
    #run to apply migrations (changes)
    #flask db upgrade
    
    #migrate = Migrate(app, db.db_instance)

    api = Api(app)

    jwt = JWTManager(app)

    @app.before_request
    def init_db():
        g.db_session = get_db_session()

    #just for testing
    @jwt.additional_claims_loader
    def add_claim_loader(identity):
        if (identity == '2'):
            return {"is_admin": True}
        
        return {"is_admin": False}

    # just for testing logout
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST

    #this is called internally by @jwt.token_in_blocklist_loader
    @jwt.revoked_token_loader
    def revoke_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has been revoked", "error": "token_revoked"}), 401
        )

    @jwt.needs_fresh_token_loader
    def fresh_token_louder(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token is not fresh", "error": "fresh+token_required"}), 401
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired", "error": "token_expired"}), 401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"message": "Request does not contain an access token", "error": "authorization_required"}), 401
        )

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

@contextmanager
def db_session():
    session = g.get("db_session")

    if session is  None:
        raise Exception("ERROR: Missing DB")

    with db.get_scoped_session(session) as _scoped_session:
        yield _scoped_session
