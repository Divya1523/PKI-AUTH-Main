from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64

def generate_proof(commit_hash, student_priv_path, instructor_pub_path):
    # 1. Load your private key
    with open(student_priv_path, "rb") as f:
        student_priv = serialization.load_pem_private_key(f.read(), password=None)

    # 2. Sign the ASCII string of the commit hash
    # CRITICAL: Use PSS, SHA256, and MAX_LENGTH salt
    signature = student_priv.sign(
        commit_hash.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # 3. Load instructor public key
    with open(instructor_pub_path, "rb") as f:
        instructor_pub = serialization.load_pem_public_key(f.read())

    # 4. Encrypt the signature with Instructor's Public Key
    # CRITICAL: Use OAEP with SHA256
    encrypted_sig = instructor_pub.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 5. Base64 encode for a single-line string
    proof_b64 = base64.b64encode(encrypted_sig).decode('utf-8')
    return proof_b64

# Usage
# commit_hash = "your_40_char_hash_here"
# print(generate_proof(commit_hash, "student_private.pem", "instructor_public.pem"))