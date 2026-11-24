import datetime

from application import interfaces
from application.dto import TransactionDTO
from domain.entities import TransactionDM
from uuid import UUID

class AddTransactionInteractor:
    def __init__(
        self,
        add_transaction: interfaces.TransactionCreator,
        category_reader: interfaces.CategoryReader,
        generate_uuid: interfaces.GenerateUUID,
    ) -> None:
        self._add_transaction = add_transaction
        self._category_reader = category_reader
        self._generate_uuid = generate_uuid

    async def __call__(
        self,
        user_id: UUID,
        dt: TransactionDTO,
    ) -> TransactionDM:

        category = await self._category_reader.read_by_category(
            user_id=user_id,
            category_id=dt.category_id,
        )

        if category is None:
            raise ValueError("Category not found")

        transaction = TransactionDM(
            id=self._generate_uuid(),
            user_id=user_id,
            category_id=dt.category_id,
            amount=dt.amount,
            description=dt.description,
            date=datetime.datetime.now(),
        )

        return await self._add_transaction.save(transaction)