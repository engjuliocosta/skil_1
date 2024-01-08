from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from accounts_payable.routers.accounts_payable import AccountsPayableResponse

router = APIRouter(
    prefix='/payment_receipts',
)


class PaymentReceiptsRequest(BaseModel):
    """Data model for payment_receipts."""
    pr_id: int
    description: str
    amount: Decimal
    date: datetime
    account_type: str


@router.post("/", response_model=List[PaymentReceiptsRequest], status_code=201)
def create_accounts_payable(receipt: PaymentReceiptsRequest):
    """Create accounts_payable:
        :post: /accounts_payable/"""
    return AccountsPayableResponse(
        pr_id=1,
        description="salario",
        value=5000,
        date="2024-01-05",
    )
