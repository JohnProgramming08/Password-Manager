from flask import Flask
from .database import db
from .routes import register_blueprints


def create_app(config_overlay=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///the_open_road.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Default configuration
    app.config.update(DEBUG=True, SECRET_KEY="67_is_still_funny_idc_what_u_say")

    # Apply test-specific overrides if they exist
    if config_overlay:
        app.config.update(config_overlay)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    register_blueprints(app)

    return app
