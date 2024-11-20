from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from .orders import Order

class PromotionBase(BaseModel):
    promotion_code: str
    expiration_date: datetime

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    promotion_code: Optional[str] = None
    expiration_date: Optional[datetime] = None

class Promotion(PromotionBase):
    id: int
    orders: Optional[List[Order]] = []

    class Config:
        from_attributes = True
