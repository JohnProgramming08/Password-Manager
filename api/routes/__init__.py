from .download import download_bp
from .upload import upload_bp


def register_blueprints(app):
    app.register_blueprint(download_bp)
    app.register_blueprint(upload_bp)
