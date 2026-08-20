from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/", response_model=TransactionResponse)
def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db)
):

    sender = db.query(Account).filter(
        Account.id == transaction_data.sender_account_id
    ).first()

    receiver = db.query(Account).filter(
        Account.id == transaction_data.receiver_account_id
    ).first()

    if not sender:
        raise HTTPException(
            status_code=404,
            detail="Sender account not found"
        )

    if not receiver:
        raise HTTPException(
            status_code=404,
            detail="Receiver account not found"
        )

    transaction = Transaction(
        sender_account_id=transaction_data.sender_account_id,
        receiver_account_id=transaction_data.receiver_account_id,
        amount=transaction_data.amount,
        payment_method=transaction_data.payment_method,
        payment_context=transaction_data.payment_context
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction