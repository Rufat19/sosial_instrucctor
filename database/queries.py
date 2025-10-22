from .db_connect import connect

# Yeni istifadəçi əlavə et
async def add_user(user_id: int, name: str, lang: str):
    conn = await connect()
    await conn.execute("""
        INSERT INTO users (user_id, name, lang)
        VALUES ($1, $2, $3)
        ON CONFLICT (user_id) DO NOTHING;
    """, user_id, name, lang)
    await conn.close()

# Bütün istifadəçiləri göstər
async def get_all_users():
    conn = await connect()
    rows = await conn.fetch("SELECT * FROM users;")
    await conn.close()
    return rows
