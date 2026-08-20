from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountResponse

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.post("/", response_model=AccountResponse)
def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db)
):
    account = Account(
        account_number=account_data.account_number,
        name=account_data.name,
        account_type=account_data.account_type
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return account