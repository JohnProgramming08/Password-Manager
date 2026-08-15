from flask import Blueprint, jsonify
from api.sync import Sync

download_bp = Blueprint("download", __name__)


# Maybe with users path as well for testing idk
# Download the data from an individual section
@download_bp.route(
    "/download_file/<password_hash>/<file_name>", methods=["POST"]
)
def download_file(password_hash: str, file_name: str):
    sync = Sync(password_hash, file_name)
    data = sync.get_section_data()
    return jsonify(data)


# Fetch all sections the user has uploaded
@download_bp.route("/list_sections/<password_hash>")
def list_sections(password_hash: str):
    sync = Sync(password_hash)
    section_list = sync.get_all_sections()

    res = {}
    for section in section_list:
        res[section] = "active"

    return jsonify(res)
