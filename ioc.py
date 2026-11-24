from collections.abc import AsyncIterable
from uuid import uuid4

from dishka import AnyOf, Provider, Scope, provide, from_context
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from application import interfaces
from application.interactors import AddTransactionInteractor
from config import Config
from infrastructure.database.database import new_session_maker
from infrastructure.database.transaction_gateways import TransactionGateway


class AppProvide(Provider):

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.GenerateUUID:
        return uuid4
    
    @provide(scope=Scope.APP)
    async def get_engine(self, config: Config) -> AsyncIterable[AsyncEngine]:
        engine, _ = new_session_maker(config.postgres)

        yield engine
        
        await engine.dispose()


    @provide(scope=Scope.APP)
    def get_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
       
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )

    @provide(scope=Scope.REQUEST)  
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:  
            yield session


    transaction_gateways = provide(
        TransactionGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            interfaces.TransactionCreator,
            interfaces.TransactionReader,
            interfaces.AllTransactionReader,
            interfaces.TransactionUpdater,
            interfaces.TransactionDeleter,
            interfaces.CategoryReader
        ]
    )

    add_transaction_interactor = provide(AddTransactionInteractor, scope=Scope.REQUEST)

    config = from_context(provides=Config, scope=Scope.APP)