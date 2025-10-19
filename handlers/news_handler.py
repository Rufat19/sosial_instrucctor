from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from database import add_news_to_db, get_all_news, get_news_by_id, get_all_users
from aiogram.filters import Command

router = Router()

# Admin komandası
@router.message(Command("add_news"), F.from_user.id == ADMIN_ID)
async def add_news(message: Message, state: FSMContext):
    # Sadə nümunə: başlıq və mətn bir mesajda göndərilsin "Başlıq | Məzmun"
    try:
        title, content = message.text.split("|", 1)
        news_id = add_news_to_db(title.strip(), content.strip(), ADMIN_ID)
        
        # Mövcud istifadəçilərə push göndər
        users = get_all_users()
        for user in users:
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Ətraflı oxu", callback_data=f"read_news:{news_id}")]
            ])
            # use message.bot to avoid circular import
            await message.bot.send_message(chat_id=user['id'], text=f"📢 {title.strip()}", reply_markup=kb)
        
        await message.answer("Yenilik əlavə olundu və istifadəçilərə göndərildi!")
    except Exception as e:
        await message.answer(f"Xəta: {e}")

# Inline button callback
@router.callback_query(F.data.startswith("read_news:"))
async def read_news_cb(query: CallbackQuery):
    news_id = int(query.data.split(":")[1])
    news = get_news_by_id(news_id)
    if news:
        await query.message.answer(f"📌 {news['title']}\n\n{news['content']}")
    await query.answer()

# "Bütün yeniliklər" buttonu
@router.message(Command("news"))
async def list_news(message: Message):
    news_list = get_all_news()
    # ensure inline_keyboard field exists for pydantic validation
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for n in news_list:
        kb.add(InlineKeyboardButton(text=n['title'], callback_data=f"read_news:{n['id']}"))
    await message.answer("Bütün yeniliklər:", reply_markup=kb)
