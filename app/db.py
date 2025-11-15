from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings

# High-performance async engine using asyncpg
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,          # keep this off for performance
    pool_size=10,        # main connection pool
    max_overflow=20,     # burst capacity under load
    future=True
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
