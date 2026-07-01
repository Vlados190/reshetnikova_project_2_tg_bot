from fastapi import FastAPI
from app.api.routes_auth import router as auth_router
from app.db_init import create_tables
import asyncio

app = FastAPI()

app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    await create_tables()