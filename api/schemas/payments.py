from typing import Optional
from pydantic import BaseModel
from .orders import Order


class PaymentBase(BaseModel):
    order_id: int
    card_information: str
    total: float
    transaction_status: str
    payment_type: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    order_id: Optional[int] = None
    card_information: Optional[str] = None
    transaction_status: Optional[str] = None
    payment_type: Optional[str] = None


class Payment(PaymentBase):
    id: int
    order: Optional[Order] = None

    class Config:
        from_attributes = True


class TotalPayments(BaseModel):
    total: float
