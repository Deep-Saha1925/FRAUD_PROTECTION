from fastapi import FastAPI

app = FastAPI(
    title="Fraud Protection System",
    description="Evidence-based fraud transaction analysis",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Fraud Protection System API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }