import hashlib

def generate_sha256_hash(password: str) -> str:
    salt = "your_salt_here"  # Add a unique salt for additional security
    combined = salt + password
    hashed = hashlib.sha256(combined.encode()).hexdigest()
    return hashed

# Example usage:
plaintext_password = "your_password_here"
hashed_password = generate_sha256_hash(plaintext_password)
print("Hashed password:", hashed_password)
