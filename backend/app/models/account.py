from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database import Base

class Account(Base):

    __tablename__ = "accounts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    account_number = Column(
        String(50),
        unique=True,
        nullable=False
    )
    name = Column(
        String(100),
        nullable=False
    )
    account_type = Column(
        String(20),
        nullable=False
    )
    status = Column(
        String(20),
        default="ACTIVE"
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )