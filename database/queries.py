import os
import json
from .db_connect import create_pool, pool

# =============================
# 🔹 İSTİFADƏÇİLƏR (PostgreSQL + JSON backup)
# =============================

USERS_FILE = os.path.join("data", "users.json")

# JSON backup üçün
def _load_users():
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] _load_users failed: {e}")
        return []

def _save_users(users):
    os.makedirs("data", exist_ok=True)
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[WARN] _save_users failed: {e}")


async def add_user(user_id: int, name: str, lang: str):
    """Yeni istifadəçi əlavə et (PostgreSQL varsa ora, yoxdursa JSON-a)."""
    try:
        if pool is None:
            await create_pool()
        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users (user_id, name, lang)
                VALUES ($1, $2, $3)
                ON CONFLICT (user_id) DO NOTHING;
            """, user_id, name, lang)
        return True
    except Exception as e:
        print(f"[WARN] add_user PostgreSQL işləmədi: {e}")
        users = _load_users()
        if not any(u["user_id"] == user_id for u in users):
            users.append({"user_id": user_id, "name": name, "lang": lang})
            _save_users(users)
        return False


async def get_all_users():
    """Bütün istifadəçiləri qaytar (PostgreSQL yoxdursa JSON-dan)."""
    try:
        if pool is None:
            await create_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT user_id, name, lang FROM users;")
            return [dict(r) for r in rows]
    except Exception as e:
        print(f"[WARN] get_all_users PostgreSQL işləmədi: {e}")
        return _load_users()


# =============================
# 🔹 YENİLİKLƏR (JSON SAXLAMA)
# =============================

NEWS_FILE = os.path.join("data", "news.json")

def _load_news():
    if not os.path.exists(NEWS_FILE):
        return []
    try:
        with open(NEWS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] _load_news failed: {e}")
        return []

def _save_news(news_list):
    os.makedirs("data", exist_ok=True)
    try:
        with open(NEWS_FILE, "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[WARN] _save_news failed: {e}")


def add_news(title: str, content: str):
    """Yeni yeniliyi əlavə et (lokal JSON saxlanma)."""
    news_list = _load_news()
    new_id = max([n["id"] for n in news_list], default=0) + 1
    news_list.append({
        "id": new_id,
        "title": title,
        "content": content
    })
    _save_news(news_list)
    print(f"[INFO] Yeni yenilik əlavə olundu: {title}")
    return new_id


def get_all_news():
    """Bütün yenilikləri al."""
    return _load_news()


def get_news_by_id(news_id: int):
    """ID-ə görə konkret yeniliyi tap."""
    for n in _load_news():
        if n["id"] == news_id:
            return n
    return None
