from fastapi import APIRouter

root_router = APIRouter(prefix="/spending")

@root_router.get("/")
async def root():
    return {"message": "Hello World"}