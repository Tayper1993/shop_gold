from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from oits.models.base import Base


class Products(Base):
    """
    Товары
    """
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(254))
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int | None] = mapped_column(Integer)
