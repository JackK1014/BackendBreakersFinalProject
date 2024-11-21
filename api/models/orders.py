from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, server_default=func.now())
    tracking_number = Column(String(100))
    order_status = Column(String(50))
    total_price = Column(DECIMAL(10, 2))
    description = Column(String(300))
    status = Column(String(50), nullable=False, default="pending")

    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)
    promotions = relationship("Promotion", secondary="order_promotions", back_populates="orders")

