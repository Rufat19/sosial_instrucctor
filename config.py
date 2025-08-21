import os
from dotenv import load_dotenv

load_dotenv()  # .env faylını oxu

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 6520873307  # Öz ID-nizi birbaşa yazın
CARD_NUMBER = os.getenv("CARD_NUMBER") or "4098 5844 6547 4300"
DB_PATH = "database.db"

if not BOT_TOKEN or not ADMIN_ID:
    raise ValueError("BOT_TOKEN və ADMIN_ID .env faylında təyin olunmalıdır.")
