from fastapi import APIRouter, UploadFile, File
from app.auth.cert_validator import validate_certificate
from app.auth.identity_hash import generate_identity_hash
from app.auth.token import generate_anonymous_token

router = APIRouter()

@router.post("/login")
async def login(cert: UploadFile = File(...)):

    cert_data = await cert.read()

    # 1. validar certificado
    identity = validate_certificate(cert_data)

    # 2. convertir a identidad irreversible
    identity_hash = generate_identity_hash(identity)

    # 3. generar token ciego
    token = generate_anonymous_token(identity_hash)

    return {
        "token": token
    }
