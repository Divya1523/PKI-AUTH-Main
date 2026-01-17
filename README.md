# PKI - Auth - System

A secure, containerized microservice demonstrating industrial security standards through Public Key Infrastructure (PKI) and Time-based One-Time Password (TOTP) authentication.

## 🛡️ Security Architecture

This project implements a multi-layered security approach to authentication:

* **Asymmetric Cryptography:** Utilizes RSA 4096-bit key pairs for secure data transmission.
* **Secure Seed Exchange:** Implementation of RSA/OAEP with SHA-256 for the decryption of sensitive authentication seeds.
* **2FA Implementation:** Standard TOTP (RFC 6238) using SHA-1, 30-second intervals, and 6-digit codes.
* **Integrity Proofs:** Commits are verified using RSA-PSS digital signatures with maximum salt length to ensure non-repudiation.

## 🏗️ Technical Stack

- **Backend:** Python (FastAPI/Uvicorn)
- **Cryptography:** `cryptography` library (Standard Python Security Provider)
- **Infrastructure:** Docker (Multi-stage builds) & Docker Compose
- **Scheduling:** Linux Cron daemon for automated background logging

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- OpenSSL (for key generation)

### Installation & Setup

1. **Clone the Repository:**
   
   git clone <your-repo-url>
   cd pki-auth-system

2. **Initialize Keys:**

   Ensure student_private.pem, student_public.pem, and instructor_public.pem are present in the root directory.

3. **Deploy with Docker:**

   docker-compose up -d --build

**Persistence & Cron**
Persistence: Decrypted seeds are stored in a named Docker volume (seed-data) mounted at /data, ensuring security credentials survive container restarts.

Background Jobs: A system-level cron job executes every minute, logging the current TOTP code to /cron/last_code.txt with UTC timestamps.

**Testing the Implementation**
To verify the system is running correctly:

1. Decrypt the Seed:
   curl -X POST http://localhost:8080/decrypt-seed -H "Content-Type: application/json" -d "{\"encrypted_seed\":\"$(cat 
   encrypted_seed.txt)\"}"

2. Verify Persistence:
   docker-compose restart && curl http://localhost:8080/generate-2fa

3. Check Cron Logs:
   docker exec pki-2fa-app cat /cron/last_code.txt

 **Features**
 Security: RSA/OAEP (SHA-256) decryption and RSA-PSS signatures.
 TOTP: RFC 6238 compliant (SHA-1, 30s window) with $\pm1$ period tolerance.
 Persistence: Docker volumes ensure seeds survive restarts.
 Automation: Cron job logs codes every minute in UTC.
