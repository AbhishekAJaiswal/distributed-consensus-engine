# crypto_utils.py

def generate_keys():
    return "private_key", "public_key"

def sign_message(private_key, message):
    return f"signed_{message}"

def verify_signature(public_key, message, signature):
    return signature == f"signed_{message}"