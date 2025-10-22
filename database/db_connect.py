import asyncpg
import os
import asyncio
from dotenv import load_dotenv

# Lokal test üçün lazımdır, Railway-də avtomatik olur
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Pool obyektini yaradırıq
pool = None

async def create_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(DATABASE_URL)
        print("🔌 Database connection pool created successfully.")
    return pool


# Sadə test funksiyası
async def test_connection():
    global pool
    if pool is None:
        await create_pool()
    async with pool.acquire() as conn:
        row = await conn.fetch("SELECT NOW();")
        print("✅ PostgreSQL connected successfully:", row)


if __name__ == "__main__":
    asyncio.run(test_connection())
