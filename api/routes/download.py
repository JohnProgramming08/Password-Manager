from flask import Blueprint, jsonify, request
from api.sync import Sync
from api.database import VerifyUser
import json

download_bp = Blueprint("download", __name__)


# Maybe with users path as well for testing idk
# Download the data from an individual section
@download_bp.route("/download_file/<email_hash>/<file_name>", methods=["POST"])
def download_file(email_hash: str, file_name: str):
    data = json.loads(request.get_json())
    password = data.get("password")

    # Ensure user details are valid
    if not VerifyUser.verify(email_hash, password):
        return jsonify({})

    # User details are valid
    sync = Sync(email_hash, file_name)
    data = sync.get_section_data()
    return jsonify(data)


# Fetch all sections the user has uploaded
@download_bp.route("/list_sections/<email_hash>", methods=["POST"])
def list_sections(email_hash: str):
    data = json.loads(request.get_json())
    password = data.get("password")

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
