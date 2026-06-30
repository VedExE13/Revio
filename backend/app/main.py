from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.db.init_db import init_db

app = FastAPI(
    title="Revio API",
    description="Backend API for Revio AI",
    version="0.1.0",
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)