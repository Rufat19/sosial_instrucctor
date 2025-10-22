# database/queries.py
from .db_connect import create_pool, pool

# Yeni istifadəçi əlavə et
async def add_user(user_id: int, name: str, lang: str):
    # Əgər pool hələ yaradılmayıbsa, yaradılır
    if pool is None:
        await create_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (user_id, name, lang)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id) DO NOTHING;
        """, user_id, name, lang)

# Bütün istifadəçiləri göstər
async def get_all_users():
    if pool is None:
        await create_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users;")
        return rows
