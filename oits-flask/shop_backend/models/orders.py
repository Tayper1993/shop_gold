from app import Base
from sqlalchemy import Column, Integer, DateTime, func, Enum, ForeignKey
from ..choices.order_status import OrderStatus


class Orders(Base):
    """Заказы"""

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    order_status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
