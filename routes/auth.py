from crypto.verify import verify_signature
from flask import Blueprint, request, jsonify
from models import db, Device, Challenge
import secrets

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/request", methods=["POST"])
def request_auth():

    data = request.get_json()

    device_id = data.get("device_id")

    if not device_id:
        return jsonify({
            "error": "device_id required"
        }), 400

    device = Device.query.filter_by(
        device_id=device_id
    ).first()

    if not device:
        return jsonify({
            "error": "Device not registered"
        }), 404

    nonce = secrets.token_hex(32)

    challenge = Challenge(
        device_id=device_id,
        nonce=nonce
    )

    db.session.add(challenge)
    db.session.commit()

    return jsonify({
        "device_id": device_id,
        "challenge": nonce
    }), 200

@auth_bp.route("/auth/verify", methods=["POST"])
def verify_auth():

    data = request.get_json()

    device_id = data.get("device_id")
    signature = data.get("signature")

    if not device_id or not signature:
        return jsonify({
            "error": "device_id and signature required"
        }), 400

    device = Device.query.filter_by(
        device_id=device_id
    ).first()

    if not device:
        return jsonify({
            "error": "Unknown device"
        }), 404

    challenge_record = (
        Challenge.query
        .filter_by(device_id=device_id)
        .order_by(Challenge.id.desc())
        .first()
    )

    if not challenge_record:
        return jsonify({
            "error": "Challenge not found"
        }), 404

    try:

        print("Challenge from DB:", challenge_record.nonce)
        print("Signature received:", signature[:60] + "...")
        print("Public key starts with:")
        print(device.public_key[:80])

        verify_signature(
            device.public_key,
            challenge_record.nonce,
            signature
        )

        return jsonify({
            "authenticated": True
        })

    except Exception as e:

        return jsonify({
            "authenticated": False,
            "error": str(e)
        }), 401