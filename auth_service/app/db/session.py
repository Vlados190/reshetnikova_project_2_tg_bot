from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

DATABASE_URL = f"sqlite+aiosqlite:///{settings.SQLITE_PATH}"

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)