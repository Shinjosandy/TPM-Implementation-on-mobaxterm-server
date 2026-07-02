from pathlib import Path

# ==========================
# Server Configuration
# ==========================

SERVER_URL = "http://10.35.40.20:8000"

# ==========================
# Device Configuration
# ==========================

DEVICE_ID = "sandhya-tpm"

# ==========================
# Project Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent

KEYS_DIR = BASE_DIR / "keys"

PUBLIC_KEY_FILE = KEYS_DIR / "public.pem"
