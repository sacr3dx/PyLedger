from backend.config import PostgresConfig
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


def new_session_maker(psql_config: PostgresConfig) -> async_sessionmaker[AsyncSession]:
   
    database_url = (
            f"postgresql+asyncpg://{psql_config.login}:"
            f"{psql_config.password}@{psql_config.host}:"
            f"{psql_config.port}/{psql_config.database}"
        )

    engine = create_async_engine(
            database_url,
            pool_size=15,
            max_overflow=15,
            connect_args={
                "command_timeout": 5,
            },
        )
    return async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)