from datetime import timedelta

from bcrypt import checkpw
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt
from sqlalchemy import DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.exceptions import Unauthorized

from oits.models.base import Base, session


class Users(Base):
    """
    Пользователь
    """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(80))
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    time_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.name = kwargs.get('name')
        self.password = bcrypt.hash(kwargs.get('password'))
        self.time_created = kwargs.get('time_created')
        self.email = kwargs.get('email')

    def get_token(self, expire_time=1):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = session.query(cls).filter(cls.email == email).first()

        if not user or not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise Unauthorized('Invalid email or password')

        return user
