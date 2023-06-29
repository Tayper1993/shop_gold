from datetime import timedelta

from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt
from sqlalchemy import create_engine, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()

engine = create_engine('postgresql+psycopg2://scot:tiger@localhost:5432/mydatabase')


class Users(Base):
    """Пользователь"""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(80))
    password_hash: Mapped[str] = mapped_column(String(120))
    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.name = kwargs.get('name')
        self.password_hash = bcrypt.hash(kwargs.get('password_hash'))
        self.time_created = kwargs.get('time_created')
        self.email = kwargs.get('email')

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('No user with this password')
        return user


class Products(Base):
    """Товары"""

    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(254))
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int | None] = mapped_column(Integer)


class Orders(Base):
    """Заказы"""

    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    order_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # order_status: Mapped[Enum] = mapped_column(Enum(OrderStatus)) TODO Сделать enum


class Payments(Base):
    """Платежи"""

    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'))
    payment_date: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), server_default=func.now())
    payment_amount: Mapped[int | None] = mapped_column(Integer)
    # payment_status: Mapped[Enum] = mapped_column(Enum()) TODO Сделать enum


class OrderHistory(Base):
    """История заказов"""

    __tablename__ = 'order_history'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)


Base.metadata.create_all(engine)
