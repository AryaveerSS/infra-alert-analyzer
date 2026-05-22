from fastapi import FastAPI
from app.routes.analyze_endpoint import router

app = FastAPI(
    title="Infrastructure Alert Analyzer",
    version="1.0.0"
)

app.include_router(router)