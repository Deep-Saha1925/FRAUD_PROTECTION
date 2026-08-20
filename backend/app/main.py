from fastapi import FastAPI

from app.database import Base, engine
from app.models import Account, Transaction

from app.routes.accounts import router as account_router
from app.routes.transactions import router as transaction_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Fraud Protection System",
    description="Evidence-based fraud transaction analysis",
    version="1.0.0"
)


# Register routes
app.include_router(account_router)
app.include_router(transaction_router)


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