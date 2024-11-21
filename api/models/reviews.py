from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    review_text = Column(String(500))
    score = Column(Integer)

    customer = relationship("Customer", back_populates="reviews")
    sandwich = relationship("Sandwich", back_populates="reviews")
