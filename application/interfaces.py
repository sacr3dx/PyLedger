from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class GenerateUUID(Protocol):
    @abstractmethod
    def __call__(self) -> UUID:
        ...

class DBSession(Protocol):
    async def commit(self) -> None:
        ...