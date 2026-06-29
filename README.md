# TPM-Based Device Authentication System

**Author:** Sandhya Chandel  
**Internship:** Bhabha Atomic Research Centre (BARC)  
**Platform:** Windows TPM 2.0 (Client) + Rocky Linux (Authentication Server)  

---

## Project Overview

This project implements an enterprise-grade **TPM-based Device Authentication System** utilizing a secure challenge-response protocol. 

The Windows client leverages the hardware-level **Trusted Platform Module (TPM 2.0)** to securely provision and store a non-exportable RSA private key. During authentication, the TPM signs a cryptographically secure, server-generated random challenge. The Rocky Linux authentication server then verifies this signature using the registered public key. 

Because the private key **never leaves the physical TPM hardware**, this architecture mitigates key-theft, cloning, and credential-spoofing attacks.

---

## Project Status

### Current Phase
* **✔ Phase 1: TPM-Based Device Authentication**
  * Achieved hardware-backed credential generation, validation, and remote attestation.

### Upcoming Phase
* **✔ Phase 2: Hybrid File Encryption using AES-256 and TPM**
  * Extending the ecosystem to leverage the authenticated enclave for secure local and remote storage orchestration.

---

## Technical Specifications & Cryptography

### Technology Stack
* **Client Environment:** Windows 10/11, .NET 8 SDK, Python 3, Microsoft Platform Crypto Provider
* **Server Environment:** Rocky Linux 9.1, Python 3.9+, Flask, Flask-SQLAlchemy, SQLite

### Cryptographic Algorithms
| Component | Algorithm / Protocol |
| :--- | :--- |
| **Key Generation** | RSA-2048 |
| **Hash Function** | SHA-256 |
| **Digital Signature** | RSA PKCS#1 v1.5 |
| **Challenge Generation** | Cryptographically Secure Random Nonce |
| **Public Key Format** | PEM (X.509 structure) |
| **Signature Encoding** | Base64 |

---

## Security Architecture Notes

* **Non-Exportable Key Storage:** The TPM private key is generated within the chip boundary and marked as non-exportable.
* **Hardware Isolation:** The private key never leaves the physical TPM hardware under any circumstances.
* **Zero-Knowledge Authentication:** Only the corresponding public key is shared and registered on the server side.
* **Anti-Replay Mechanism:** Every individual authentication request triggers a fresh, cryptographically random challenge on the server.
* **Cryptographic Integrity:** Strict challenge-response verification is enforced using robust RSA-SHA256 digital signatures.

---

## Project Structure

```text
TPM Implementation/
│
├── app.py
├── config.py
├── client_config.py
├── models.py
├── requirements.txt
│
├── crypto/
│   └── verify.py
│
├── routes/
│   ├── auth.py
│   └── register.py
│
├── device/
│   ├── authenticate.py
│   ├── register_device.py
│   ├── tpm_sign.py
│   ├── export_tpm_public_key.py
│   ├── provision.py
│   └── __init__.py
│
├── keys/
│   ├── public.pem
│   └── tpm_public.pem
│
├── TpmSigner/
│   ├── Program.cs
│   └── TpmSigner.csproj
│
└── README.md

```

---

## Database Schema

The authentication server utilizes an **SQLite** engine managed via Flask-SQLAlchemy to persist device enrollment and state tracking information.

### Tables

1. **`devices`**
* *Purpose:* Stores information about registered hardware endpoints.
* *Fields:* Tracks metadata such as unique `device_id` identifiers and the corresponding cryptographic `public_key` payloads.


2. **`challenges`**
* *Purpose:* Tracks volatile session nonces.
* *Fields:* Manages actively generated tokens, linking specific issued challenges back to requesting devices to protect against timing and replay vectors.



---

## TPM Signer Execution Flow

The interaction loop translates higher-level Python workflows into low-level hardware interactions:

* **Step 1:** The Python script calls the C# TPM Signer executable.
* **Step 2:** The C# TPM Signer interacts with the TPM via the Microsoft Platform Crypto Provider.
* **Step 3:** The TPM hardware performs the internal RSA signature operation using its non-exportable private key.
* **Step 4:** The C# TPM Signer encodes the resulting binary signature into a Base64 string and returns it to Python.
* **Step 5:** Python sends this Base64 signature to the remote authentication server for validation.

---

## Authentication Sequence Diagram

```text
  Windows Client             Authentication Server
        │                              │
        │─── Request Challenge ───────>│
        │    (device_id)               │
        │                              │
        │                              │─── Generate Random Nonce
        │                              │
        │<── Return Random Nonce ──────│
        │    (challenge)               │
        │                              │
  ───┐  │                              │
  │  │  │                              │
  TPM Signs Challenge                  │
  │  │  │                              │
  └──▶  │                              │
        │─── Submit Signature ────────>│
        │    (device_id, signature)    │
        │                              │
        │                              │─── Verify Signature
        │                              │    (via Public Key)
        │                              │
        │<── Auth Status (200 OK) ─────│
        │    (authenticated: true)     │
        │                              │

```

---

## Centralized Client Configuration

All endpoint configuration options are managed inside a single file: **`client_config.py`**. You do not need to hunt down configurations across multiple scripts.

Before running execution tasks, modify these specific values to fit your network layout:

* **`SERVER_URL`**: The remote target Flask API endpoint base path (e.g., `http://10.35.40.20:8000`).


* **`DEVICE_ID`**: The unique identifier tag assigned to the local hardware client environment.


* **`PUBLIC_KEY_FILE`**: The local resolution path pointing to the exported public key certificate asset.



---

## Deployment & Setup

### Rocky Linux Server Environment Setup

Install native package bindings along with the Python context dependencies:

```bash
# Prepare project sandbox directory
mkdir ~/tpm_server
cd ~/tpm_server

```

Move the server-side modules (`app.py`, `config.py`, `models.py`, `requirements.txt`, `routes/`, `crypto/`) onto this node.

### Windows Client Environment Setup

* Ensure the **.NET 8 SDK** environment toolchain is active.


* Provision your TPM-backed RSA cryptographic key container using the assembly binaries.



---

## Execution Instructions

> **Note on Command Formatting:** Always execute client scripts using the module flag format (`python -m package.module`) rather than directly calling relative file targets (e.g., `python device\register_device.py`). Executing with `-m` ensures that Python handles module resolution and absolute package pathways correctly from the project root directory, avoiding namespace lookup and relative import anomalies.
> 
> 

### Step 1: Initialize the Authentication Server (Rocky Linux Node)

```bash
cd ~/tpm_server
python3 app.py

```

*Expected console telemetry:* `* Running on http://10.35.40.20:8000/`

### Step 2: Validate Server Health

From an alternate console interface session, poll the baseline diagnostic checkpoint endpoint:

```bash
curl [http://10.35.40.20:8000/](http://10.35.40.20:8000/)

```

*Expected Response structural array:*

```json
{
    "project": "TPM Authentication Server",
    "status": "Running"
}

```

### Step 3: Device Registration Pipeline (Windows Host)

Open a target command interface terminal container centered within your base installation hierarchy:

```cmd
cd "C:\Users\BARC\Desktop\TPM\TPM Implementation"
python -m device.register_device

```

*Expected Pipeline Output response state:* `Status Code: 201 | Device registered successfully`

### Step 4: Perform Device Authentication Challenge Flow

```cmd
python -m device.authenticate

```

*Expected Execution Output Trace:*

```text
[1] Requesting challenge...
[✓] Challenge received

[2] Signing challenge...
[✓] Signature generated

[3] Verifying authentication...

========================
Authentication Result
========================

Challenge : Verified
Signature : Valid

RESULT : AUTHENTICATED

```

### Isolated Subsystem Verification (C# Module Verification)

To debug signature mechanics independently from the remote pipeline wrapper scripts:

```cmd
cd TpmSigner
dotnet run -- "hello"

```

---

## API Reference Documentation

### 1. Root Status Check

* **Method:** `GET`
* **Endpoint:** `/`

* **Description:** Returns the operational condition status of the Flask backend container pipeline.

### 2. Endpoint Enrollment

* **Method:** `POST`
* **Endpoint:** `/register`

* **Payload Schema:**

```json
{
    "device_id": "sandhya-tpm",
    "public_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...\n-----END PUBLIC KEY-----"
}

```

### 3. Session Challenge Request

* **Method:** `POST`
* **Endpoint:** `/auth/request`

* **Payload Schema:**

```json
{
    "device_id": "sandhya-tpm"
}

```

* **Response Schema:**

```json
{
    "challenge": "b96a4f8c2b740e5d836101a9"
}

```

### 4. Remote Attestation Verification

* **Method:** `POST`
* **Endpoint:** `/auth/verify`

* **Payload Schema:**

```json
{
    "device_id": "sandhya-tpm",
    "signature": "MIIEPgIBAAKCAQEA03Y5vG..."
}

```

* **Response Schema:**

```json
{
    "authenticated": true
}

```

---

## Diagnostics & Troubleshooting

### Target Server Engine Dependency Verification

Verify runtime environment modules on the Linux server using these direct validation hooks:

```bash
# Check Flask Framework Integration
python3 -c "import flask; print(flask.__version__)"

# Check ORM Persistence Interconnection Integration
python3 -c "from flask_sqlalchemy import SQLAlchemy; print('OK')"

# Check System Boundary Port Configurations
ss -tulpn | grep 8000

```

### Common Resolutions

* **Error Connection Refused / Connection Timeout Error:**

* Verify routing access logic. Run a direct validation port poll (`ss -tulpn | grep 8000`) on the target endpoint interface engine to make sure the app pipeline is active. Restart execution bounds using `python3 app.py`.




* **Routing Resulting in 404 Endpoint Frame Failures:**

* Query the internal Flask path-mapping configuration registry structure matrix directory context to confirm structural correctness:




```bash
python3 -c "from app import app; print(app.url_map)"

```



---

## Future Enhancements

* **Hybrid AES-256 File Encryption:** Implement hybrid encryption schemes combining asymmetric key pairs with fast symmetric stream algorithms.
* **TPM-Protected AES Key Wrapping:** Secure the localized data vault layer by sealing symmetric block cipher operational credentials natively within the secure memory layout boundaries of the cryptographic chip.
* **Secure File Decryption & In-Memory Processing:** Prevent exposure vectors across secondary block tracking systems during translation pipelines.
* **Secure File Deletion:** Enforce non-recoverable block wiping protocols directly linked to key lifecycle management.
* **File Integrity Verification:** Integrate baseline cryptographic signature checking components into local client file states.
* **Enterprise GUI Application:** Transition functional automation from a command-line interface layout matrix into a secure graphical desktop application dashboard framework environment.
