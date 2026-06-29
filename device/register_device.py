from pathlib import Path
import requests


from client_config import SERVER_URL, DEVICE_ID, PUBLIC_KEY_FILE

def load_public_key():
    with open(PUBLIC_KEY_FILE, "r") as f:
        return f.read()


def register_device():

    if not PUBLIC_KEY_FILE.exists():
        print("[ERROR] public.pem not found")
        print("Run provision.py first")
        return

    public_key = load_public_key()

    payload = {
        "device_id": DEVICE_ID,
        "public_key": public_key
    }

    try:

        response = requests.post(
            f"{SERVER_URL}/register",
            json=payload,
            timeout=10
        )

        print("\nStatus Code:", response.status_code)

        try:
            print("Response:", response.json())
        except Exception:
            print("Response:", response.text)

    except Exception as e:
        print(f"Registration failed: {e}")
        print(str(e))


if __name__ == "__main__":
    register_device()