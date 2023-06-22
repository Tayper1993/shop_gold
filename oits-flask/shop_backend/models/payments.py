from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey

Base = declarative_base()


class Payments(Base):
    """Платежи"""

    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    payment_amount = Column(Integer)
    payment_status = Column(Integer)
