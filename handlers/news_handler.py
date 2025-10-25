from aiogram import Router, F
from aiogram.types import (
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    CallbackQuery
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from config import ADMIN_ID
from database import add_news_to_db, get_all_news, get_news_by_id, get_all_users

router = Router()

# FSM mərhələləri
class AddNewsState(StatesGroup):
    waiting_for_title = State()
    waiting_for_content = State()


# 🔹 Admin "Yenilik əlavə et" əmri ilə prosesi başladır
@router.message(Command("add_news"))
async def start_add_news(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Bu əmri yalnız admin yaza bilər.")
    
    await message.answer("📝 Yeniliyin başlığını daxil et:")
    await state.set_state(AddNewsState.waiting_for_title)


# 🔹 Başlıq daxil edilir
@router.message(AddNewsState.waiting_for_title)
async def get_news_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("📄 İndi isə yeniliyin məzmununu yaz:")
    await state.set_state(AddNewsState.waiting_for_content)


# 🔹 Məzmun daxil edilir və DB-yə yazılır
@router.message(AddNewsState.waiting_for_content)
async def save_news_content(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data["title"]
    content = message.text

    # DB-yə yazırıq
    news_id = await add_news_to_db(title, content, message.from_user.id)
    await state.clear()

    # Bütün istifadəçilərə push göndəririk
    users = await get_all_users()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Ətraflı oxu", callback_data=f"read_news:{news_id}")]
        ]
    )

    for user in users:
        try:
            await message.bot.send_message(
                chat_id=user["id"], 
                text=f"📢 *{title}*\nYeni yenilik əlavə olundu!",
                reply_markup=kb,
                parse_mode="Markdown"
            )
        except Exception:
            continue  # bəziləri block edə bilər, o zaman keç

    await message.answer("✅ Yenilik əlavə olundu və bütün istifadəçilərə göndərildi.")


# 🔹 Xəbəri oxumaq üçün inline düymə
@router.callback_query(F.data.startswith("read_news:"))
async def read_news_cb(query: CallbackQuery):
    news_id = int(query.data.split(":")[1])
    news = await get_news_by_id(news_id)
    if not news:
        return await query.answer("Xəbər tapılmadı.", show_alert=True)
    
    await query.message.answer(
        f"📌 *{news['title']}*\n\n{news['content']}",
        parse_mode="Markdown"
    )
    await query.answer()


# 🔹 "Bütün yeniliklər" komandası
@router.message(Command("news"))
async def list_news(message: Message):
    news_list = await get_all_news()
    if not news_list:
        return await message.answer("Hələlik yenilik yoxdur.")

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=n["title"], callback_data=f"read_news:{n['id']}")] for n in news_list
    ])

    await message.answer("📰 Bütün yeniliklər:", reply_markup=kb)


# 🔹 "Yeniliklər" inline düyməsi (start.py-dən çağırmaq üçün)
@router.callback_query(F.data == "show_news")
async def show_news_from_inline(query: CallbackQuery):
    news_list = await get_all_news()
    if not news_list:
        return await query.answer("Hələlik yenilik yoxdur.", show_alert=True)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=n["title"], callback_data=f"read_news:{n['id']}")] for n in news_list
    ])
    await query.message.answer("📰 Bütün yeniliklər:", reply_markup=kb)
    await query.answer()
