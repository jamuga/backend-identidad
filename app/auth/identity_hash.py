import hmac
import hashlib
import os


# 🔐 CLAVE SECRETA SOLO EN VM1 (NO EN GIT)
SECRET_KEY = os.environ.get("IDENTITY_SECRET_KEY")

if not SECRET_KEY:
    raise Exception("Missing IDENTITY_SECRET_KEY env variable")


def normalize_dn(dn: str) -> str:
    """
    Normaliza el DN para evitar duplicados por formato
    """
    return dn.strip().lower()


def generate_global_identity(dn: str) -> str:
    """
    Convierte DN → ID global irreversible
    """

    normalized = normalize_dn(dn)

    return hmac.new(
        SECRET_KEY.encode(),
        normalized.encode(),
        hashlib.sha256
    ).hexdigest()
