from fastapi import FastAPI
from app.api.routes import health

app = FastAPI(title="Data Audit API")

app.include_router(health.router)


@app.get("/")
def root():
    return {"message": "Data Audit API running"}
