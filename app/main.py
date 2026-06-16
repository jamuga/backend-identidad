from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from app.api.routes import router

app = FastAPI(title="Backend Identidad")

app.include_router(router)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):

    public_paths = ["/"]

    if any(request.url.path.startswith(p) for p in public_paths):
        return await call_next(request)

    # permitir estáticos/templates sin romper login
    if request.url.path.startswith("/static"):
        return await call_next(request)

    if not request.cookies.get("global_id"):
        return RedirectResponse("https://sondeoelectoralreal.es/")

    return await call_next(request)