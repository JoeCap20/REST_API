import os
# This URL will show the Stores REST API http://localhost:5000/swagger-ui
# #Better to define a function whos job it is to create and setup and configure the flask app. call this function in order to test.
# #This is what the factory pattern looks like
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

import models

from db import db
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    api = Api(app)

    #When the users sends one back to tell us who they are the app can check 
    #the secret key and use it to verify that this app created that JWT Therefore it is valid
    #Used to make sure the user hasnt created their own JWT somewhere else and is pretedning to be the one we want
    #Keep the secret key safe and have it be a random long generated key

    #This line below would change the secret key every time which is something we dont want to do. We want to gernate it and then use that single one 
    #app.config["JWT_SECRET_KEY"] = secrets.SystemRandom().getrandbits(128)

    #One way is run python, then import secrets, then secrets.SystemRandom().getrandbits(128) then copy the output

    app.config["JWT_SECRET_KEY"] = "jose"
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app