import secrets

# Generate a secure random 256-bit (32-byte) key
secret_key = secrets.token_hex(32)
print(secret_key)