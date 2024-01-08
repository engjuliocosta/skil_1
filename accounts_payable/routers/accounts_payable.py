from typing import List

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from accounts_payable.models.accounters import Accounters as Acc
from shared.dependencies import get_db

router = APIRouter(
    prefix='/accounts_payable',
)


class AccountsPayableResponse(BaseModel):
    """Data model for accounts_payable."""
    id: int
    description: str
    value: float
    account_type: str

    class Config:
        orm_mode = True


class AccountsPayableRequest(BaseModel):
    """Data model for accounts created for payment."""
    description: str
    value: float
    account_type: str


@router.get("/", response_model=List[AccountsPayableResponse])
def list_accounts_payable(db: Session = Depends(get_db)) -> List[AccountsPayableResponse]:
    """List accounts_payable:
        :return: list of accounts_payable;
        :get: /accounts_payable"""
    return db.query(Acc).all()


# TODO: Implementar melhor a busca para resultar em uma lista de accounts_payable no Swagger
@router.post("/", response_model=AccountsPayableResponse, status_code=201)
def create_accounts_payable(account: AccountsPayableRequest,
                            db: Session = Depends(get_db)) -> AccountsPayableResponse:
    """Create accounts_payable:
        :post: /accounts_payable"""

    account_payd = Acc(
        **{}
    )

    db.add(account_payd)
    db.commit()
    db.refresh(account_payd)

    return account_payd
