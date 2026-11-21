from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import PostgresConfig


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

    session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False
    )

    return engine, session_maker

async def check_engine(engine: AsyncEngine) -> None:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
        
    print("Database connection successful")    

async def check_migrations(engine: AsyncEngine) -> None:
    async with engine.connect() as connection:
        result = await connection.execute(
            text("SELECT version_num FROM alembic_version")
        )
        current_revision = result.scalar_one_or_none()

    if current_revision is None:
        raise RuntimeError("Database migrations are not applied")

    print(f"Current migration: {current_revision}")