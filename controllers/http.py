from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from uuid import UUID

from application.dto import TransactionDTO
from application.interactors import AddTransactionInteractor
from domain.entities import TransactionDM

transaction_router = APIRouter(prefix="/transaction", route_class=DishkaRoute, tags=["Transaction_functions"])

#before JWT auth
def user_get() -> UUID:
    return UUID("11111111-1111-4111-8111-111111111111")

@transaction_router.post("/add_transaction")
async def add_transaction(
        data: TransactionDTO,
        interactor: FromDishka[AddTransactionInteractor]
) -> TransactionDM:

    dto = TransactionDTO(
        category_id=data.category_id,
        amount=data.amount,
        description=data.description
    )

    result = await interactor(
        user_id=user_get(),
        dt=dto)
    return result