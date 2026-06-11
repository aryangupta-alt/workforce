from fastapi import FastAPI

from backend.routes.report import router

app = FastAPI(
    title="Workforce Intelligence API"
)

app.include_router(router)