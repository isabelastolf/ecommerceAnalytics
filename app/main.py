from fastapi import FastAPI
from app.api.routes import health
from app.api import analytics

import app.models

app = FastAPI(title="Data Audit API")

app.include_router(health.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "Data Audit API running"}
