from flask import Blueprint, jsonify
from api.sync import Sync
from api.database import VerifyUser

download_bp = Blueprint("download", __name__)


# Maybe with users path as well for testing idk
# Download the data from an individual section
@download_bp.route(
    "/download_file/<email_hash>/<password>/<file_name>", methods=["POST"]
)
def download_file(email_hash: str, password: str, file_name: str):
    # Ensure user details are valid
    if not VerifyUser.verify(email_hash, password):
        return jsonify({})

    # User details are valid
    sync = Sync(email_hash, file_name)
    data = sync.get_section_data()
    return jsonify(data)


# Fetch all sections the user has uploaded
@download_bp.route("/list_sections/<email_hash>/<password>", methods=["POST"])
def list_sections(email_hash: str, password: str):
    # Ensure user details are valid
    if not VerifyUser.verify(email_hash, password):
        return jsonify({})

    # User details are valid
    sync = Sync(email_hash)
    section_list = sync.get_all_sections()

    res = {}
    for section in section_list:
        res[section] = "active"

    return jsonify(res)
