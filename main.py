from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from config import Config
from infrastructure.database.database import check_engine, check_migrations
from ioc import AppProvide
from routers.main_page import root_router

config = Config()
container = make_async_container(AppProvide(), context={Config: config})


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        engine = await container.get(AsyncEngine)

        await check_engine(engine)
        await check_migrations(engine)

        yield
    finally:
        await container.close()

def get_app() -> FastAPI:
    app = FastAPI(title="PyLedger", lifespan=lifespan)
    app.include_router(root_router)

    setup_dishka(container, app)
    return app

app = get_app()