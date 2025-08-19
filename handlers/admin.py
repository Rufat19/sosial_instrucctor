from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
import datetime

router = Router()

def log_history(user_id, action):
    with open("user_history.log", "a", encoding="utf-8") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{user_id}|{action}|{now}\n")

# Demo üçün tarixçə (realda DB-dən və ya fayldan oxuya bilərsən)
USER_HISTORY = [
    {"user_id": 213213913, "action": "PDF endir", "date": "2024-08-10"},
    {"user_id": 987654321, "action": "Qeydiyyat", "date": "2024-08-09"},
    # TODO: Real tarixçə əlavə et
]

@router.message(F.text == "/admin")
async def admin_panel(message: Message, state: FSMContext):
    if not message.from_user or message.from_user.id != ADMIN_ID:
        await message.answer("Bu funksiya yalnız admin üçün aktivdir.")
        return
    try:
        with open("user_start_history.log", "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            await message.answer("Heç bir istifadəçi tarixçəsi yoxdur.")
            return
        history_text = "<b>Botu işə salan istifadəçilər:</b>\n"
        for line in lines[-50:]:  # Son 50 istifadəçi
            user_id, date = line.strip().split("|")
            history_text += f"Telegram İD: <code>{user_id}</code> — {date}\n"
        await message.answer(history_text, parse_mode="HTML")
    except Exception as e:
        await message.answer(f"Tarixçə oxunmadı: {e}")



