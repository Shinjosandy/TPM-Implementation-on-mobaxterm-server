# TPM-Based Device Authentication Server (Option 1)

## Overview

This project implements a challenge-response authentication framework using public key cryptography. The system allows devices to register their public keys, request authentication challenges, sign those challenges using their private keys, and authenticate themselves through cryptographic signature verification.

This implementation serves as the foundation for future TPM-based authentication and remote attestation.

\---

## Features

* Device Registration
* Public Key Storage
* Challenge Generation
* Challenge Storage
* Digital Signature Verification
* Challenge-Response Authentication
* SQLite Database Integration
* Flask REST APIs

\---

## Technology Stack

* Python 3
* Flask
* Flask-SQLAlchemy
* SQLite
* OpenSSL
* Postman
* Visual Studio Code

\---

## Project Structure

```text
tpm-auth-server/

├── app.py
├── config.py
├── models.py
├── requirements.txt
├── database.db

├── routes/
│   ├── register.py
│   └── auth.py

├── crypto/
│   ├── challenge.py
│   └── verify.py

├── keys/
│   ├── private.pem
│   └── public.pem

└── device/
```

\---

# Server Setup

## Create Project Directory

```powershell
mkdir tpm-auth-server
cd tpm-auth-server
```

## Create Virtual Environment

```powershell
python -m venv venv
```

## Activate Virtual Environment

```powershell
.\\\\venv\\\\Scripts\\\\Activate.ps1
```

If PowerShell blocks execution:

```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (\\\& .\\\\venv\\\\Scripts\\\\Activate.ps1)
```

\---

## Install Dependencies

```powershell
pip install flask
pip install flask-sqlalchemy
pip install cryptography
pip install pyjwt
pip install requests
```

Save installed packages:

```powershell
pip freeze > requirements.txt
```

\---

## Create Project Folders

```powershell
mkdir routes
mkdir crypto
mkdir device
mkdir keys
```

\---

## Start Server

```powershell
python app.py
```

Expected Output:

```text
\\\* Running on http://127.0.0.1:5000
```

\---

# RSA Key Generation

Navigate to the keys directory:

```powershell
cd keys
```

Generate a private key:

```powershell
openssl genrsa -out private.pem 2048
```

Generate the corresponding public key:

```powershell
openssl rsa -in private.pem -pubout -out public.pem
```

Verify OpenSSL installation:

```powershell
openssl version
```

Display the public key:

```powershell
Get-Content public.pem -Raw
```

\---

# API Testing Using Postman

## 1\. Register Device

### Endpoint

```http
POST /register
```

### Request Body

```json
{
  "device\\\_id": "sandhya1234",
  "public\\\_key": "-----BEGIN PUBLIC KEY-----\\\\n...\\\\n-----END PUBLIC KEY-----"
}
```

### Successful Response

```json
{
  "message": "Device registered successfully"
}
```

\---

## 2\. Request Authentication Challenge

### Endpoint

```http
POST /auth/request
```

### Request Body

```json
{
  "device\\\_id": "sandhya1234"
}
```

### Example Response

```json
{
  "device\\\_id": "sandhya1234",
  "challenge": "316c48754b7e42fd9f24a669b7dd75d05aed683df513cdf3ef50d4fa584db3fd"
}
```

Copy the challenge value.

\---

# Generate Digital Signature

Create a challenge file:

```powershell
notepad challenge.txt
```

Paste the challenge string received from the server and save.

Sign the challenge:

```powershell
openssl dgst -sha256 -sign private.pem -out signature.bin challenge.txt
```

Convert signature to Base64:

```powershell
certutil -encode signature.bin signature.txt
```

Open the generated file:

```powershell
notepad signature.txt
```

Copy only the Base64 content between the BEGIN and END markers.

\---

# Verify Authentication

## Endpoint

```http
POST /auth/verify
```

## Request Body

```json
{
  "device\\\_id": "sandhya1234",
  "signature": "<Base64 Signature>"
}
```

## Successful Response

```json
{
  "authenticated": true
}
```

\---

# Authentication Workflow

```text
Device Registration
       │
       ▼
Store Public Key
       │
       ▼
Request Challenge
       │
       ▼
Generate Nonce
       │
       ▼
Sign Challenge
       │
       ▼
Submit Signature
       │
       ▼
Verify Signature
       │
       ▼
Authentication Success
```

\---

# Security Features

* Public Key Cryptography
* Challenge-Response Authentication
* Replay Attack Prevention
* Server-Side Signature Verification
* Private Key Isolation

\---

# Current Status

### Completed

* Flask Server
* SQLite Database
* Device Registration
* Challenge Generation
* Signature Verification
* End-to-End Authentication

### Planned (Option 2)

* TPM Endorsement Key (EK)
* Attestation Identity Key (AIK)
* TPM Quote Verification
* PCR Validation
* Remote Attestation
* TPM-Based Device Trust Verification

\---

# Future Work

The current implementation uses software-generated RSA keys. In the next phase, the private key will be replaced by a TPM-protected key, enabling hardware-backed authentication and remote attestation.

