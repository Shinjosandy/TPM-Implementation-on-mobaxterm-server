from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import base64


def verify_signature(public_key_pem, challenge, signature_b64):

    signature = base64.b64decode(signature_b64)

    public_key = serialization.load_pem_public_key(
        public_key_pem.encode()
    )

    public_key.verify(
        signature,
        challenge.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    return True