from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="GitHub Actions Docker Demo",
    description="A small FastAPI service built and tested by GitHub Actions.",
    version="1.0.0",
)

@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "Hello from Docker!",
        "service": "github-actions-docker-demo",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
