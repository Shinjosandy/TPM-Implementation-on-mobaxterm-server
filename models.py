from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)

    device_id = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    public_key = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Challenge(db.Model):
    __tablename__ = "challenges"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    device_id = db.Column(
        db.String(100),
        nullable=False
    )

    nonce = db.Column(
        db.String(256),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )