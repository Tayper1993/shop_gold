from sqlalchemy import DateTime, ForeignKey, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from oits.models.base import Base


class Orders(Base):
    """
    Заказы
    """
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    order_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
