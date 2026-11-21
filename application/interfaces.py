from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from domain.entities import TransactionDM


class GenerateUUID(Protocol):
    @abstractmethod
    def __call__(self) -> UUID:
        ...

class DBSession(Protocol):
    async def commit(self) -> None:
        ...

class TransactionCreator(Protocol):
    @abstractmethod
    async def save(
        self,
        user_id: UUID,
        transaction: TransactionDM
    ) -> TransactionDM: 
        ...
class TransactionUpdater(Protocol):
    @abstractmethod
    async def update(
        self,
        user_id: UUID,
        uuid: UUID,
        transaction: TransactionDM
    ) -> None:
        ...

class TransactionDeleter(Protocol):
    @abstractmethod
    async def del_by_uuid(
        self,
        uuid: UUID,
        user_id: UUID
    ) -> str | None:
        ...

class TransactionReader(Protocol):
    @abstractmethod
    async def read_by_uuid(
        self,
        user_id: UUID,
        uuid: UUID
    ) -> TransactionDM | None:
        ...

class AllTransactionReader(Protocol):
    @abstractmethod
    async def read_all(
        self,
        user_id: UUID
    ) -> list[TransactionDM]:
        ...

