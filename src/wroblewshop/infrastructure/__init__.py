from typing import List

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserEntity(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(Text)
    cupboard_id: Mapped[int] = mapped_column(ForeignKey("cupboard.id"), nullable=False)
    cupboard: Mapped["CupboardEntity"] = relationship(back_populates="users")


class CupboardEntity(Base):
    __tablename__ = "cupboard"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    users: Mapped["UserEntity"] = relationship(back_populates="cupboard")
    items: Mapped[List["ItemEntity"]] = relationship()


class ItemEntity(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    cupboard_id: Mapped[int] = mapped_column(ForeignKey("cupboard.id"), nullable=False)
