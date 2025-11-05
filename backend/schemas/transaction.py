from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator
from datetime import datetime
from enum import Enum

class PaymentMode(str,Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    NET_BANKING = "NET_BANKING"
    UPI = "UPI"
    CASH = "CASH"
    CHEQUE = "CHEQUE"    

class CreateTransaction(BaseModel):
    bank_transaction_id : str | None = None
    payment_mode : PaymentMode = PaymentMode.CHEQUE
    amount_paid : float
    description: str| None = None
    payment_date: datetime
    bill_id: int

class UpdateTransaction(BaseModel):
    id: int
    bank_transaction_id : str | None = None
    payment_mode : PaymentMode | None = None
    amount_paid : float | None = None
    description: str| None = None
    payment_date: datetime | None = None
    bill_id: int | None = None

class ShowTransaction(CreateTransaction):
    id: int
    model_config = ConfigDict(from_attributes=True)   
