from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

BASE_DIR = Path(__file__).resolve().parent.parent

KEYS_DIR = BASE_DIR / "keys"

PRIVATE_KEY_FILE = KEYS_DIR / "private.pem"
PUBLIC_KEY_FILE = KEYS_DIR / "public.pem"


def keys_exist():
    return (
        PRIVATE_KEY_FILE.exists()
        and PUBLIC_KEY_FILE.exists()
    )


def generate_keys():

    print("[*] Generating RSA key pair...")

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    KEYS_DIR.mkdir(exist_ok=True)

    with open(PRIVATE_KEY_FILE, "wb") as f:
        f.write(private_pem)

    with open(PUBLIC_KEY_FILE, "wb") as f:
        f.write(public_pem)

    print("[✓] Keys generated successfully")


if __name__ == "__main__":

    if keys_exist():
        print("[✓] Keys already exist")
    else:
        generate_keys()