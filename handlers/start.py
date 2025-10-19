from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
import datetime
from database.db import add_user
from database import get_all_news
from utils.logger_utils import log_event
from config import ADMIN_ID

router = Router()


@router.callback_query(F.data == "channels")
async def channels_callback(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Sosial Mühit", callback_data="channel_sosial_muhit")]
        ]
    )
    if callback.message is not None:
        await callback.message.answer("Kanal seçin:", reply_markup=keyboard)
    await callback.answer()

def log_user_start(user_id):
    with open("user_start_history.log", "a", encoding="utf-8") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{user_id}|{now}\n")

def get_main_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚡ Əmsal Oyunu", callback_data="fast_test_start")],
            [InlineKeyboardButton(text="🏆 Ən yaxşı kanalı seç! 🏆", callback_data="channel_access_menu")],
            [InlineKeyboardButton(text="🌍 Dünya Görüşü- quiz paketlər", callback_data="quiz_world_menu")],
            [InlineKeyboardButton(text="📊 Power BI Sertifikat Testləri", callback_data="cert_menu")],
            [InlineKeyboardButton(text="📦 Sosial ödənişlər- quiz paketlər", callback_data="quiz")],
            [InlineKeyboardButton(text="📄 Müsahibələrə Hazırlıq Texnikası", callback_data="get_pdf")],
            [InlineKeyboardButton(text="� Yeniliklər", callback_data="news_menu")],
            [InlineKeyboardButton(text="�🕹️ Komanda Köstəbək Oyunu", callback_data="game_info")],
            [InlineKeyboardButton(text="🛠️ Bot sifarişi (depozit)", callback_data="order_bot")],
            [InlineKeyboardButton(text="💰 RBCron balansım", callback_data="balance_menu")],
            [InlineKeyboardButton(text="🌟 İstifadəçi rəyləri", callback_data="reviews_menu")],
            [InlineKeyboardButton(text="ℹ️ Qəbul Mərkəzləri haqqında", callback_data="about_bot")]
        ]
    )

@router.message(F.text == "/start")
async def start_menu(message: Message, state: FSMContext):
    if message.chat.type == "private":
        if message.from_user is not None:
            log_user_start(message.from_user.id)
            add_user(message.from_user.id, message.from_user.username or "")
            # log activity for analytics — build a robust display name
            try:
                user = message.from_user
                # prefer full_name, fallback to first + last, then username
                display_name = None
                if hasattr(user, "full_name") and user.full_name:
                    display_name = user.full_name
                else:
                    parts = [p for p in (getattr(user, "first_name", ""), getattr(user, "last_name", "")) if p]
                    display_name = " ".join(parts) if parts else (getattr(user, "username", "") or "")

                lang = getattr(user, "language_code", None) or "unknown"
                log_event(user.id, display_name, "start", lang)
                # Notify admin about new user start (non-blocking)
                try:
                    if ADMIN_ID:
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        admin_text = (
                            f"🔔 Yeni istifadəçi botu işə saldı:\n"
                            f"👤 {display_name or user.username or user.id} (id: {user.id})\n"
                            f"🕒 {now}\n"
                            f"🌐 lang: {lang}"
                        )
                        await message.bot.send_message(ADMIN_ID, admin_text)
                except Exception:
                    # don't break user flow if admin notify fails
                    pass
            except Exception:
                # don't break the handler if logging fails
                pass
        await message.answer("Aşağıdakı seçimlərdən birini seçin və bütün funksiyalara rahat giriş əldə edin:", reply_markup=get_main_buttons())
    else:
        if message.from_user is not None:
            await message.reply(
                "ℹ️ Botun əsas menyusunu açmaq üçün şəxsi mesajda (/start) yazın.\n\n👉 <a href='https://t.me/Allien_BiBOT" + (message.bot.username if hasattr(message.bot, 'username') else "") + "'>Botu aç</a>",
                parse_mode="HTML"
            )

main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⚡ Texniki biliklərini sınağa çək (Eng)", callback_data="fast_test_start")],
        [InlineKeyboardButton(text="🏆 Ən yaxşı kanalı seç! 🏆", callback_data="channel_access_menu")],
        [InlineKeyboardButton(text="🌍 Dünya Görüşü- quiz paketlər", callback_data="quiz_world_menu")],
        [InlineKeyboardButton(text="📊 Power BI Sertifikat Testləri", callback_data="cert_menu")],
        [InlineKeyboardButton(text="📦 Sosial ödənişlər- quiz paketlər", callback_data="quiz")],
        [InlineKeyboardButton(text="📄 Müsahibələrə Hazırlıq Texnikası", callback_data="get_pdf")],
        [InlineKeyboardButton(text="🕹️ Komanda Köstəbək Oyunu", callback_data="game_info")],
        [InlineKeyboardButton(text="🛠️ Bot sifarişi (depozit)", callback_data="order_bot")],
        [InlineKeyboardButton(text="💰 RBCron balansım", callback_data="balance_menu")],
        [InlineKeyboardButton(text="🌟 İstifadəçi rəyləri", callback_data="reviews_menu")],
        [InlineKeyboardButton(text="ℹ️ Bot haqqında məlumat", callback_data="about_bot")]
    ]
)

@router.callback_query(F.data == "back")
async def back_callback(callback: CallbackQuery, state: FSMContext):
    if callback.message is not None:
        await callback.message.answer("Aşağıdakı seçimlərdən birini seçin və bütün funksiyalara rahat giriş əldə edin:", reply_markup=get_main_buttons())
    await callback.answer()

@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery, state: FSMContext):
    if callback.message is not None:
        await callback.message.answer("Aşağıdakı seçimlərdən birini seçin və bütün funksiyalara rahat giriş əldə edin:", reply_markup=get_main_buttons())
    await callback.answer()


@router.callback_query(F.data == "news_menu")
async def news_menu_callback(callback: CallbackQuery):
    news_list = get_all_news()
    # pydantic requires inline_keyboard field; pass empty list if no buttons
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for n in news_list:
        kb.add(InlineKeyboardButton(text=n['title'], callback_data=f"read_news:{n['id']}"))
    if callback.message is not None:
        await callback.message.answer("Bütün yeniliklər:", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data == "balance_menu")
async def balance_menu_callback(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Balansı göstər", callback_data="show_balance")],
            [InlineKeyboardButton(text="Balansı doldur", callback_data="fill_balance")],
            [InlineKeyboardButton(text="🏠 Əsas menyuya qayıt", callback_data="main_menu")]
        ]
    )
    if callback.message is not None:
        await callback.message.answer("Balans menyusu:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "channel")
async def channel_callback(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Sosial Mühit", callback_data="channel_sosial_muhit")]
        ]
    )
    if callback.message is not None:
        await callback.message.answer("Kanal seçin:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "game_info")
async def game_info_callback(callback: CallbackQuery):
    if callback.message is not None:
        await callback.message.answer(
            "🕹️ Komanda köstəbək oyunu üçün qrupda /game yazın.\n"
            "Ən azı 3 nəfər olmalıdır. Qaydalar: Hamıya bir söz, birinə fərqli söz. Sonda səsvermə!\n\n"
            "Komandan yoxdursa, narahat olma! 🎉\n"
            "Səni və dostlarını əyləncəli və maraqlı bir oyun üçün Köstəbəksən Telegram qrupuna dəvət edirik: https://t.me/kostebeksen\n"
            "Burada yeni insanlarla tanış ol, birgə oynamağın dadını çıxar və özünü sınaya bilərsən."
        )
    await callback.answer()