from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Products(Base):
    """Товары"""

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(254))
    price = Column(Integer)
    quantity = Column(Integer)
