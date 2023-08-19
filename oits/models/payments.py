from sqlalchemy import DateTime, ForeignKey, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from oits.models.base import Base


class Payments(Base):
    """
    Платежи
    """

    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'))
    payment_date: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), server_default=func.now())
    payment_amount: Mapped[int | None] = mapped_column(Integer)
