import uuid
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UsersModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[str] = mapped_column(DateTime)

    categories: Mapped[list["CategoriesModel"]] = relationship(
        back_populates="user"
        )
    
    transactions: Mapped[list["TransactionsModel"]] = relationship(
        back_populates="user"
    )

class CategoriesModel(Base):
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
        )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False) 
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(10))

    user: Mapped["UsersModel"] = relationship(
    back_populates="categories"
    )

    transactions: Mapped[list["TransactionsModel"]] = relationship(
        back_populates="category"
    )


class TransactionsModel(Base): 
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False) 
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    date: Mapped[str] = mapped_column(DateTime)

    user: Mapped["UsersModel"] = relationship(
        back_populates="transactions"
    )

    category: Mapped["CategoriesModel"] = relationship(
        back_populates="transactions"
    )