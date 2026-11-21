from collections.abc import AsyncIterable
from uuid import uuid4

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from application import interfaces
from config import Config
from infrastructure.database.database import new_session_maker


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
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[  
        AsyncSession,  
        interfaces.DBSession,  
    ]]:  
        async with session_maker() as session:  
            yield session
