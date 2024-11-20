from typing import Optional
from pydantic import BaseModel
from .customers import Customer
from .sandwiches import Sandwich

class ReviewBase(BaseModel):
    customer_id: int
    sandwich_id: int
    review_text: Optional[str] = None
    score: Optional[int] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    customer_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    review_text: Optional[str] = None
    score: Optional[int] = None

class Review(ReviewBase):
    id: int
    customer: Optional[Customer] = None
    sandwich: Optional[Sandwich] = None

    class Config:
        from_attributes = True
