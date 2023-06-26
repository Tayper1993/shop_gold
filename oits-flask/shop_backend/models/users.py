from app import Base
from sqlalchemy import Column, Integer, String, DateTime, func


class User(Base):
    """Пользователь"""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)
    name = Column(String(80))
    password = Column(String(254))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    email = Column(String(120), unique=True, nullable=False)
