from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(slots=True)
class UserCreateDTO:
    username: str
    email: str
    hashed_password: str

@dataclass(slots=True)
class UserDTO:
    id: UUID
    username: str
    email: str

@dataclass(slots=True)
class CategoriesDTO:
    name: str
    type: str

@dataclass(slots=True)
class TransactionsDTO:
    category_id: UUID
    amount: Decimal
    description: str | None
