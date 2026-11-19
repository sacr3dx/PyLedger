from fastapi import FastAPI

from routers.main_page import root_router


def get_app() -> FastAPI:
    app = FastAPI(title="PyLedger")
    app.include_router(root_router)
    return app

app = get_app()