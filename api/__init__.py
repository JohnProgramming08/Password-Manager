import os
from dotenv import load_dotenv
from flask import Flask
from .routes import register_blueprints
from .database import db


def create_app(config_overlay=None):
    load_dotenv()
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("database_uri")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Default configuration
    app.config.update(DEBUG=True, SECRET_KEY=os.getenv("secret_key"))

    # Apply test-specific overrides if they exist
    if config_overlay:
        app.config.update(config_overlay)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    register_blueprints(app)

    return app
