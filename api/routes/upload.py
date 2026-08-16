from flask import Blueprint, request, jsonify
from api.sync import Sync
from api.database import VerifyUser

upload_bp = Blueprint("upload", __name__)


# Maybe with users path as well for testing idk
@upload_bp.route(
    "/upload/<email_hash>/<password>/<file_name>", methods=["POST"]
)
def upload(email_hash: str, password: str, file_name: str):
    file_contents = request.get_json()

    # Ensure user details are valid
    if not VerifyUser.verify(email_hash, password):
        return jsonify({})

    # User details are valid
    sync = Sync(email_hash, file_name, file_contents)
    sync.upload_data()

    return jsonify({"ok": True})
