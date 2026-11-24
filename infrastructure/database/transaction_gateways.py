from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces import (
    AllTransactionReader,
    TransactionCreator,
    TransactionDeleter,
    TransactionReader,
    TransactionUpdater,
    CategoryReader
)
from domain import entities
from domain.entities import TransactionDM
from infrastructure.database.models import TransactionsModel, CategoriesModel


class TransactionGateway(
    TransactionCreator,
    TransactionReader,
    AllTransactionReader,
    TransactionUpdater,
    TransactionDeleter,
    CategoryReader
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def read_by_category(
        self,
        user_id: UUID,
        category_id: UUID
    ) -> entities.CategoryDM | None:
        result = await self._session.execute(
            select(CategoriesModel).where(
                CategoriesModel.id == category_id,
                CategoriesModel.user_id == user_id
            )
        )

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return entities.CategoryDM(
            id=model.id,
            user_id=model.user_id,
            name = model.name,
            type = model.type
        )


    async def save(
        self,
        transaction: entities.TransactionDM
        ) -> entities.TransactionDM:
        model = TransactionsModel(
            id=transaction.id,
            user_id=transaction.user_id,
            category_id=transaction.category_id,
            amount=transaction.amount,
            description=transaction.description,
            date=transaction.date
        )
        self._session.add(model)
        await self._session.commit()

        return transaction

    async def update(
        self,
        user_id: UUID,
        uuid: UUID,
        transaction: TransactionDM
    ) -> None:
        ...

    async def del_by_uuid(
        self,
        uuid: UUID,
        user_id: UUID
    ) -> str | None:
        ...

    async def read_by_uuid(
            self,
            user_id: UUID,
            uuid: UUID
    ) -> TransactionDM | None:
        ...

    async  def read_all(
        self,
        user_id: UUID
    ) -> list[TransactionDM]:
        ...