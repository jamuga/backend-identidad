from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.auth.identity_hash import generate_global_identity
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

API_VOTACION_URL = os.getenv("API_VOTACION_URL", "https://sondeoelectoralreal.es")
API_KEY = os.getenv("API_KEY", "")


@router.get("/", response_class=HTMLResponse)
def landing():
    return """
    <html>
        <body style="background:#0f172a;color:white;text-align:center;padding-top:100px">
            <h1>Sistema de voto</h1>
            <a href="https://login.sondeoelectoralreal.es/auth/me">Login con certificado</a>
        </body>
    </html>
    """


@router.get("/auth/me")
def auth_me(request: Request):

    dn = request.headers.get("X-SSL-Client-DN")
    verify = request.headers.get("X-SSL-Client-Verify")

    if not dn or verify != "SUCCESS":
        return RedirectResponse("https://sondeoelectoralreal.es/")

    global_id = generate_global_identity(dn)

    response = RedirectResponse("https://sondeoelectoralreal.es/votacion")

    response.set_cookie(
        key="global_id",
        value=global_id,
        httponly=True,
        secure=True,
        samesite="Lax",
        domain=".sondeoelectoralreal.es"
    )

    return response


@router.get("/votacion", response_class=HTMLResponse)
def votacion(request: Request):

    global_id = request.cookies.get("global_id")

    if not global_id:
        return RedirectResponse("https://sondeoelectoralreal.es/")

    with open("app/static/votacion.html", "r") as f:
        html = f.read()

    html = html.replace("__GLOBAL_ID__", global_id)
    html = html.replace("__API_URL__", API_VOTACION_URL)
    html = html.replace("__API_KEY__", API_KEY)

    return HTMLResponse(content=html)