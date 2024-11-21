from datetime import datetime
from typing import Optional
from pydantic import BaseModel,Field, field_validator
from .order_details import OrderDetail



class OrderBase(BaseModel):
    customer_id: int
    customer_name: str
    tracking_number: Optional[str] = None
    order_status: Optional[str] = None
    total_price: Optional[float] = None
    description: Optional[str] = None
    status: str = "pending"

class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    tracking_number: Optional[str] = None
    order_status: Optional[str] = None
    total_price: Optional[float] = None
    description: Optional[str] = None
    status: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: str = Field(..., alias="order_date", description="Formatted order date")
    order_details: list[OrderDetail] = None

    @field_validator("order_date", mode="before")
    def format_order_date(cls, value):
        """Format the order_date field to a string."""
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value

    class Config:
        from_attributes = True
