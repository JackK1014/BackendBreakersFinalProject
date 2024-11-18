from datetime import datetime
from typing import Optional
from pydantic import BaseModel,Field
from .order_details import OrderDetail



class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: str = Field(..., alias="order_date", description="Formatted order date")
    order_details: list[OrderDetail] = None

    @staticmethod
    def format_datetime(value: datetime) -> str:
        """Format datetime to be a user friendly string."""
        return value.strftime("%B %d, %Y, %I:%M %p")
    class ConfigDict:
        from_attributes = True
