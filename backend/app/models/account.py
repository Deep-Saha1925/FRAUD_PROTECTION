from pydantic import BaseModel

class AccountCreate(BaseModel):
    account_number: str
    name: str
    account_type: str


class AccountResponse(BaseModel):
    id: int
    account_number: str
    name: str
    account_type: str
    status: str

    class Config:
        from_attributes = True