from flask import Blueprint, request, jsonify
from api.sync import Sync

upload_bp = Blueprint("upload", __name__)


# Maybe with users path as well for testing idk
@upload_bp.route("/upload/<password_hash>/<file_name>", methods=["POST"])
def upload(password_hash: str, file_name: str):
    file_contents = request.get_json()
    sync = Sync(password_hash, file_name, file_contents)
    sync.upload_data()

    return jsonify({"ok": True})
