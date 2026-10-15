from fastapi import FastAPI

from app.core.config import settings
from app.routers import productos

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(productos.router)


@app.get("/")
def inicio():
    return {"mensaje": "Hola, FastAPI"}
