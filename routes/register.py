from flask import Blueprint, request, jsonify
from models import db, Device

register_bp = Blueprint("register", __name__)


@register_bp.route("/register", methods=["POST"])
def register_device():

    data = request.get_json()

    device_id = data.get("device_id")
    public_key = data.get("public_key")

    if not device_id or not public_key:
        return jsonify({
            "error": "device_id and public_key required"
        }), 400

    existing_device = Device.query.filter_by(
        device_id=device_id
    ).first()

    if existing_device:
        return jsonify({
            "message": "Device already registered"
        }), 409

    device = Device(
        device_id=device_id,
        public_key=public_key
    )

    db.session.add(device)
    db.session.commit()

    return jsonify({
        "message": "Device registered successfully"
    }), 201