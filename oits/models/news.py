from sqlalchemy import DateTime, ForeignKey, func, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from oits.models.base import Base


class News(Base):
    """
    Новости
    """

    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    publication_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
