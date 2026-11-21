from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(slots=True)
class UserDM:
    id: UUID
    username: str
    email: str
    hashed_password: str
    created_at: datetime

@dataclass(slots=True)
class CategoriesDM:
    id: UUID
    user_id: UUID
    name: str
    type: str

@dataclass(slots=True)
class TransactionsDM:
    id: UUID
    user_id: UUID
    category_id: UUID
    amount: Decimal
    description: str | None
    date: datetime
