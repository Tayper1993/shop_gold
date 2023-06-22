from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, ForeignKey

Base = declarative_base()


class OrderHistory(Base):
    """История заказов"""

    __tablename__ = 'order_history'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    price = Column(Integer)
