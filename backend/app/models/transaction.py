from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func
from app.database import Base

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    sender_account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )
    receiver_account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )
    amount = Column(
        Numeric(12, 2),
        nullable=False
    )
    payment_method = Column(
        String(30),
        nullable=False
    )
    payment_context = Column(
        String(30),
        default="UNKNOWN"
    )
    status = Column(
        String(20),
        default="COMPLETED"
    )
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )