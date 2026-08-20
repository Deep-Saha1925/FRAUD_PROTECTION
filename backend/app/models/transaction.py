from pydantic import BaseModel
from decimal import Decimal


class TransactionCreate(BaseModel):
    sender_account_id: int
    receiver_account_id: int
    amount: Decimal
    payment_method: str
    payment_context: str = "UNKNOWN"


class TransactionResponse(BaseModel):
    id: int
    sender_account_id: int
    receiver_account_id: int
    amount: Decimal
    payment_method: str
    payment_context: str
    status: str

    class Config:
        from_attributes = True