from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.models.transaction import Transaction

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/")
def create_transaction(
    sender_account_id: int,
    receiver_account_id: int,
    amount: float,
    payment_method: str,
    payment_context: str = "UNKNOWN",
    db: Session = Depends(get_db)
):

    sender = db.query(Account).filter(
        Account.id == sender_account_id
    ).first()

    receiver = db.query(Account).filter(
        Account.id == receiver_account_id
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
        sender_account_id=sender_account_id,
        receiver_account_id=receiver_account_id,
        amount=amount,
        payment_method=payment_method,
        payment_context=payment_context
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction