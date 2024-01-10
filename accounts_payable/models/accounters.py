from sqlalchemy import Column, Integer, String, Numeric
from shared.dbhandler import Base


class Accounters(Base):
    """Models for accounters."""
    __tablename__ = "accounters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(30))
    value = Column(Numeric)
    account_type = Column(String(30))
