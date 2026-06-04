from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.auth.identity_hash import generate_global_identity
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

API_VOTACION_URL = os.getenv("API_VOTACION_URL")
API_KEY = os.getenv("API_KEY")
IDENTITY_SALT = os.getenv("IDENTITY_SALT")


# -------------------------
# LANDING (SIN CERTIFICADO)
# -------------------------
@router.get("/", response_class=HTMLResponse)
def landing():

    return """
    <html>
        <head>
            <title>Sistema de Voto Anónimo</title>
            <style>
                body {
                    font-family: Arial;
                    background: #0f172a;
                    color: white;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }

                .container {
                    margin-top: 120px;
                }

                h1 {
                    font-size: 40px;
                }

                p {
                    color: #94a3b8;
                    font-size: 18px;
                }

                .btn {
                    margin-top: 30px;
                    padding: 14px 28px;
                    font-size: 18px;
                    background: #3b82f6;
                    border: none;
                    border-radius: 8px;
                    color: white;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                }

                .btn:hover {
                    background: #2563eb;
                }
            </style>
        </head>

        <body>
            <div class="container">
                <h1>Sistema de Voto Anónimo</h1>
                <p>Accede con tu certificado digital FNMT</p>

                <a class="btn" href="/auth/me">
                    Login con certificado
                </a>
            </div>
        </body>
    </html>
    """


@router.get("/auth/me", response_class=HTMLResponse)
def me(request: Request):

    dn = request.headers.get("X-SSL-Client-DN")
    verify = request.headers.get("X-SSL-Client-Verify")

    if not dn or verify != "SUCCESS":
        return "<h1>Acceso denegado</h1>"

    global_id = generate_global_identity(dn)

    return f"""
    <html>
    <head>
        <title>Votación</title>
        <style>
            body {{
                font-family: Arial;
                background: #0f172a;
                color: white;
                text-align: center;
                margin-top: 80px;
            }}

            button {{
                padding: 15px 25px;
                margin: 10px;
                font-size: 18px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }}

            .pp {{ background: #3b82f6; }}
            .psoe {{ background: #ef4444; }}
            .vox {{ background: #22c55e; }}

            .modal {{
                display: none;
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: rgba(0,0,0,0.7);
            }}

            .modal-content {{
                background: white;
                color: black;
                padding: 20px;
                margin: 15% auto;
                width: 300px;
                border-radius: 10px;
            }}
        </style>
    </head>

    <body>

        <h1>Sistema de Votación</h1>
        <p>ID: {global_id[:12]}...</p>

        <button class="pp" onclick="openModal('pp')">PP</button>
        <button class="psoe" onclick="openModal('psoe')">PSOE</button>
        <button class="vox" onclick="openModal('vox')">VOX</button>

        <div id="modal" class="modal">
            <div class="modal-content">
                <h3 id="modalText"></h3>
                <button onclick="confirmVote()">Confirmar</button>
                <button onclick="closeModal()">Cancelar</button>
            </div>
        </div>

        <script>
            let selectedParty = "";
            const GLOBAL_ID = "{global_id}";

            function openModal(party) {{
                selectedParty = party;
                document.getElementById("modalText").innerText =
                    "Confirmar voto a " + party.toUpperCase();
                document.getElementById("modal").style.display = "block";
            }}

            function closeModal() {{
                document.getElementById("modal").style.display = "none";
            }}

            async function confirmVote() {{

                console.log("CLICK OK", selectedParty);

                try {{

                    const res = await fetch("{API_VOTACION_URL}/vote", {{
                        method: "POST",
                        headers: {{
                            "Content-Type": "application/json",
                            "x-api-key": "{API_KEY}"
                        }},
                        body: JSON.stringify({{
                            global_id: GLOBAL_ID,
                            party: selectedParty
                        }})
                    }});

                    const text = await res.text();
                    console.log("RESPUESTA:", text);

                    closeModal();

                }} catch (e) {{
                    console.error("ERROR:", e);
                }}
            }}
        </script>

    </body>
    </html>
    """
