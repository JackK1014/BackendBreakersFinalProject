from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

order_promotions = Table(
    'order_promotions', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('promotion_id', Integer, ForeignKey('promotions.id'))
)


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promotion_code = Column(String(50), unique=True, nullable=False)
    expiration_date = Column(DateTime, nullable=False)

    orders = relationship("Order", secondary=order_promotions, back_populates="promotions")
