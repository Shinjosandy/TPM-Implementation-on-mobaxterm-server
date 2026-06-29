from cryptography import x509
from cryptography.hazmat.primitives import serialization
from pathlib import Path
from client_config import PUBLIC_KEY_FILE

cert_file = Path.home() / "Desktop" / "BARC-TPM.cer"

with open(cert_file, "rb") as f:
    cert = x509.load_der_x509_certificate(f.read())

public_key = cert.public_key()

pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

output_file = Path(__file__).resolve().parent.parent / "keys" / "tpm_public.pem"

with open(output_file, "wb") as f:
    f.write(pem)

print("TPM public key exported:")
print(output_file)