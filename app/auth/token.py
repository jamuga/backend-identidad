import hmac
import hashlib
import os

SECRET = os.environ.get("TOKEN_SECRET", "change_this_token_secret")

def generate_anonymous_token(identity_hash: str) -> str:
    return hmac.new(
        SECRET.encode(),
        identity_hash.encode(),
        hashlib.sha256
    ).hexdigest()
