import time

from fastapi import FastAPI, Depends, Request
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .db import get_db
from .models import User, Order

app = FastAPI()

@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    # simple DB round-trip test
    result = await db.execute(text("SELECT 1"))
    return {"db": result.scalar(), "status": "ok"}


@app.get("/perf/ping")
async def perf_ping():
    return {"msg": "ok"}


@app.get("/perf/db-real/{user_id}")
async def perf_db_real(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.orders).selectinload(Order.items)
        )
    )
    result = await db.execute(stmt)
    return result.scalars().first()

request_count = 0
last_reset = time.time()

# Track timestamps of requests
request_timestamps = []

@app.middleware("http")
async def count_requests(request: Request, call_next):
    global request_timestamps

    # Record the time when request starts
    now = time.time()
    request_timestamps.append(now)

    # Clean up old timestamps older than 60 seconds
    cutoff = now - 60
    request_timestamps = [t for t in request_timestamps if t >= cutoff]

    return await call_next(request)
