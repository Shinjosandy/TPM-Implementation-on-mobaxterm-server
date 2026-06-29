import requests

from client_config import SERVER_URL, DEVICE_ID
from .tpm_sign import tpm_sign


def request_challenge():

    response = requests.post(
        f"{SERVER_URL}/auth/request",
        json={
            "device_id": DEVICE_ID
        }
    )

    response.raise_for_status()

    return response.json()["challenge"]


def sign_challenge(challenge):

    return tpm_sign(challenge)


def verify_authentication(signature_b64):

    response = requests.post(
        f"{SERVER_URL}/auth/verify",
        json={
            "device_id": DEVICE_ID,
            "signature": signature_b64
        }
    )

    return response

def main():

    print("\n[1] Requesting challenge...")

    challenge = request_challenge()

    print("[✓] Challenge received")
    print("Challenge:", challenge)

    print("\n[2] Signing challenge...")

    signature = sign_challenge(challenge)

    print("[✓] Signature generated")

    print("\n[3] Verifying authentication...")

    response = verify_authentication(signature)
    result = response.json()

    print("\n========================")
    print("Authentication Result")
    print("========================")

    print(f"Device ID : {DEVICE_ID}")

    if result.get("authenticated"):
        print("Challenge : Verified")
        print("Signature : Valid")
        print("\n✅ RESULT : AUTHENTICATED")
    else:
        print("Challenge : Verification Failed")
        print("Signature : Invalid")
        print("\n❌ RESULT : NOT AUTHENTICATED")
        if "error" in result:
            print("Reason:", result["error"])

    print("================================")


if __name__ == "__main__":
    main()