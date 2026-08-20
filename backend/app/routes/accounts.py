from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.post("/")
def create_account(
    account_number: str,
    name: str,
    account_type: str,
    db: Session = Depends(get_db)
):

    account = Account(
        account_number=account_number,
        name=name,
        account_type=account_type
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return account