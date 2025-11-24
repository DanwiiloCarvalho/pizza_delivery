from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean
from core.settings import settings as stt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.order import Order


class User(stt.DBBaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(150), nullable=False)

    email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False)

    password: Mapped[str] = mapped_column(String(150), nullable=False)

    active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    orders: Mapped[list['Order']] = relationship(
        back_populates='user', lazy='joined')

    def __repr__(self):
        return f'Username: {self.name}\nemail: {self.email}'
