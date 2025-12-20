from fastapi import FastAPI

from app.core.database import engine, Base
from app.models import user, task
from app.api.router import router

app = FastAPI(title="Todo List", version="1.0.0", description="FastAPI Todo List API")

Base.metadata.create_all(engine)

app.include_router(
    router,
    prefix="/api",
)
