import asyncio
import httpx
import time
import random

URL = "http://localhost:8000/perf/db-real/{user_id}"
CONCURRENCY = 200   # number of parallel workers
DURATION = 10       # seconds
USER_ID_MAX = 5000  # adjust based on your DB

async def worker(client):
    count = 0
    end_time = time.time() + DURATION
    while time.time() < end_time:
        user_id = random.randint(1, USER_ID_MAX)        # pick random user
        url = URL.format(user_id=user_id)               # inject user_id

        try:
            await client.get(url)
            count += 1
        except Exception:
            pass  # ignore failures for now
    return count

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [worker(client) for _ in range(CONCURRENCY)]
        results = await asyncio.gather(*tasks)

    total = sum(results)
    rps = total / DURATION

    print(f"Total requests: {total}")
    print(f"Requests per second: {rps}")
    print(f"Requests per minute: {rps * 60}")

if __name__ == "__main__":
    asyncio.run(main())
