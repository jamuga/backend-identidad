import hashlib
import os

SECRET = os.environ.get("IDENTITY_SECRET", "change_this_super_secret")

def generate_identity_hash(identity: str) -> str:
    data = (SECRET + identity).encode()
    return hashlib.sha256(data).hexdigest()
