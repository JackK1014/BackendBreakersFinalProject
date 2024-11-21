from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    card_information = Column(String(100))
    transaction_status = Column(String(50))
    payment_type = Column(String(50))

    order = relationship("Order", back_populates="payment")
