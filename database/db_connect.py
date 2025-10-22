import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()  # Railway-də avtomatik olacaq, amma local test üçün vacibdir

DATABASE_URL = os.getenv("DATABASE_URL")

async def connect():
    conn = await asyncpg.connect(DATABASE_URL)
    return conn
