import os
from dotenv import load_dotenv
from flask import Flask
from .routes import register_blueprints


def create_app(config_overlay=None):
    load_dotenv()
    app = Flask(__name__)

    # Default configuration
    app.config.update(DEBUG=True, SECRET_KEY=os.getenv("secret_key"))

    # Apply test-specific overrides if they exist
    if config_overlay:
        app.config.update(config_overlay)

    register_blueprints(app)

    return app
