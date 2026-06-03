from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Backend Identidad - Voto Anónimo")

app.include_router(router)

@app.get("/")
def health():
    return {"status": "ok"}
