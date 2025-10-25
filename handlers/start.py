from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
import datetime
from database.queries import add_user  # ✅ PostgreSQL üçün
from utils.logger_utils import log_event
from config import ADMIN_ID

router = Router()


# Kanal seçimi callback
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


# İstifadəçi start tarixçəsini log fayla yazır
def log_user_start(user_id):
    with open("user_start_history.log", "a", encoding="utf-8") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{user_id}|{now}\n")


# Əsas menyu düymələri
def get_main_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚡ Əmsal Oyunu", callback_data="fast_test_start")],
            [InlineKeyboardButton(text="🏆 Ən yaxşı kanalı seç! 🏆", callback_data="channel_access_menu")],
            [InlineKeyboardButton(text="🌍 Dünya Görüşü- quiz paketlər", callback_data="quiz_world_menu")],
            [InlineKeyboardButton(text="📊 Power BI Sertifikat Testləri", callback_data="cert_menu")],
            [InlineKeyboardButton(text="📦 Sosial ödənişlər- quiz paketlər", callback_data="quiz")],
            [InlineKeyboardButton(text="📄 Müsahibələrə Hazırlıq Texnikası", callback_data="get_pdf")],
            [InlineKeyboardButton(text="🆕 Yeniliklər", callback_data="news_menu")],
            [InlineKeyboardButton(text="🕹️ Komanda Köstəbək Oyunu", callback_data="game_info")],
            [InlineKeyboardButton(text="🛠️ Bot sifarişi (depozit)", callback_data="order_bot")],
            [InlineKeyboardButton(text="💰 RBCron balansım", callback_data="balance_menu")],
            [InlineKeyboardButton(text="🌟 İstifadəçi rəyləri", callback_data="reviews_menu")],
            [InlineKeyboardButton(text="ℹ️ Qəbul Mərkəzləri haqqında", callback_data="about_bot")]
        ]
    )


# /start komandası
@router.message(F.text == "/start")
async def start_menu(message: Message, state: FSMContext):
    if message.chat.type == "private":
        if message.from_user is not None:
            log_user_start(message.from_user.id)

            # ✅ PostgreSQL-ə yazırıq
            try:
                await add_user(
                    user_id=message.from_user.id,
                    name=message.from_user.full_name or message.from_user.username or "Unknown",
                    lang=message.from_user.language_code or "unknown"
                )
            except Exception as e:
                print(f"[DB ERROR] add_user failed: {e}")

            # Aktivlik logu
            try:
                user = message.from_user
                display_name = user.full_name or user.username or str(user.id)
                lang = getattr(user, "language_code", None) or "unknown"
                log_event(user.id, display_name, "start", lang)

                # Adminə məlumat
                if ADMIN_ID:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    admin_text = (
                        f"🔔 Yeni istifadəçi botu işə saldı:\n"
                        f"👤 {display_name} (id: {user.id})\n"
                        f"🕒 {now}\n"
                        f"🌐 lang: {lang}"
                    )
                    try:
                        await message.bot.send_message(ADMIN_ID, admin_text)
                    except Exception:
                        pass
            except Exception as e:
                print(f"[LOG ERROR] {e}")

        await message.answer(
            "Aşağıdakı seçimlərdən birini seçin və bütün funksiyalara rahat giriş əldə edin:",
            reply_markup=get_main_buttons()
        )
    else:
        if message.from_user is not None:
            await message.reply(
                "ℹ️ Botun əsas menyusunu açmaq üçün şəxsi mesajda (/start) yazın.\n\n👉 "
                f"<a href='https://t.me/{message.bot.username}'>Botu aç</a>",
                parse_mode="HTML"
            )


# Əlavə əsas menyu variantı
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


# Geri qayıt callback
@router.callback_query(F.data == "back")
async def back_callback(callback: CallbackQuery, state: FSMContext):
    if callback.message is not None:
        await callback.message.answer(
            "Aşağıdakı seçimlərdən birini seçin və bütün funksiyalara rahat giriş əldə edin:",
            reply_markup=get_main_buttons()
        )
    await callback.answer()


# Əsas menyuya qayıt callback
@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery, state: FSMContext):
    if callback.message is not None:
        await callback.message.answer(
            "Aşağıdakı seçimlərdən birini seçin və bütün funksiyalara rahat giriş əldə edin:",
            reply_markup=get_main_buttons()
        )
    await callback.answer()


# ✅ YENİLİKLƏR (tam işlək versiya)
@router.callback_query(F.data == "news_menu")
async def news_menu_callback(callback: CallbackQuery):
    from database.queries import get_all_news  # circular import-un qarşısı üçün

    try:
        news_list = await get_all_news()  # ✅ await əlavə edildi
    except Exception as e:
        await callback.message.answer(f"⚠️ Xəbərləri yükləmək mümkün olmadı:\n{e}")
        await callback.answer()
        return

    if not news_list:
        await callback.message.answer("Hələlik heç bir yenilik əlavə edilməyib.")
        await callback.answer()
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for n in news_list:
        kb.inline_keyboard.append([
            InlineKeyboardButton(text=n['title'], callback_data=f"read_news:{n['id']}")
        ])

    await callback.message.answer("📰 Son yeniliklər:", reply_markup=kb)
    await callback.answer()


# ✅ Xəbəri oxuma callback
@router.callback_query(F.data.startswith("read_news:"))
async def read_news_callback(callback: CallbackQuery):
    from database.queries import get_news_by_id

    try:
        news_id = int(callback.data.split(":")[1])
        news = await get_news_by_id(news_id)
        if not news:
            await callback.message.answer("Bu xəbər tapılmadı və ya silinib.")
            return

        await callback.message.answer(
            f"📰 <b>{news['title']}</b>\n\n{news['content']}",
            parse_mode="HTML"
        )
    except Exception as e:
        await callback.message.answer(f"⚠️ Xəbəri oxumaq mümkün olmadı:\n{e}")
    await callback.answer()


# Balans menyusu
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


# Kanal seçimi
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


# Oyun məlumatı
@router.callback_query(F.data == "game_info")
async def game_info_callback(callback: CallbackQuery):
    if callback.message is not None:
        await callback.message.answer(
            "🕹️ Komanda köstəbək oyunu üçün qrupda /game yazın.\n"
            "Ən azı 3 nəfər olmalıdır. Qaydalar: Hamıya bir söz, birinə fərqli söz. Sonda səsvermə!\n\n"
            "Komandan yoxdursa, narahat olma! 🎉\n"
            "Səni və dostlarını əyləncəli və maraqlı bir oyun üçün Köstəbəksən Telegram qrupuna dəvət edirik:\n"
            "👉 https://t.me/kostebeksen\n\n"
            "Burada yeni insanlarla tanış ol, birgə oynamağın dadını çıxar və özünü sınaya bilərsən."
        )
    await callback.answer()
