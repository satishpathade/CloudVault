# app/routes/upload_routes.py

from flask import Blueprint, request, jsonify, render_template
import uuid

from app.services.s3_service import generate_presigned_upload_url
from app.services.db_service import save_file_metadata

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@upload_bp.route("/api/uploads/presigned-url", methods=["POST"])
def create_upload_url():
    try:
        data = request.get_json(silent=True)

        if not data or "filename" not in data:
            return jsonify({
                "error": "filename is required"
            }), 400

        filename = data["filename"]
        content_type = request.headers.get(
            "Content-Type",
            "application/octet-stream"
        )

        object_key = f"user-uploads/{uuid.uuid4()}-{filename}"

        upload_url = generate_presigned_upload_url(
            object_key
        )

        save_file_metadata(filename, object_key)

        return jsonify({
            "uploadUrl": upload_url,
            "objectKey": object_key
        })

    except Exception as e:
        return jsonify({
            "error": "Failed to generate upload URL",
            "details": str(e)
        }), 500
