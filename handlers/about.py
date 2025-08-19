from handlers.start import get_main_buttons
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import asyncio
from handlers.start import main_menu_keyboard

router = Router()

def get_text(key: str) -> str:
    texts = {
        "about_bot_info": (
            "<b>Alien_BiBOT — Sənin Telegram dünyandakı köməkçin!</b>\n\n"
            "🌟 <b>Rəyini paylaş, ulduzla qiymətləndir!</b> — Öz fikrini bildir, başqalarının təcrübəsini oxu, admin cavabını birbaşa al!\n\n"
            "🕹️ <b>Köstəbək Oyunu</b> — Dostlarınla əylən, impostoru tap, qrupda səsvermə və həyəcan dolu anlar yaşa!\n\n"
            "📄 <b>PDF-lər və faydalı materiallar</b> — Bir kliklə eksklüziv PDF-ləri əldə et, balansdan RBCron çıxılır!\n\n"
            "💰 <b>Balansını izlə və artır</b> — Hesabındakı RBCronu rahatlıqla yoxla və artır!\n\n"
            "🚀 <b>Qeydiyyat və giriş</b> — Bir neçə saniyəyə qeydiyyatdan keç, unikal linkini əldə et və sosial mühitə qoşul!\n\n"
            "📢 <b>Faydalı kanallar</b> — Ən maraqlı və faydalı Telegram kanallarına birbaşa giriş!\n\n"
            "👀 <b>Bütün istifadəçi rəyləri</b> — İstənilən vaxt başqalarının təcrübəsini oxu!\n\n"
            "🤖 <b>Bot haqqında</b> — Bütün imkanlar bir yerdə!\n\n"
            "<b>Niyə Alien_BiBOT?</b>\n"
            "• Sürətli və rahat interfeys\n"
            "• Tam təhlükəsizlik və şəffaflıq\n"
            "• Adminlə birbaşa əlaqə və dəstək\n"
            "• Maraqlı dizayn və smayliklərlə zəngin menyu\n"
            "• Hər kəs üçün əlçatan və istifadəsi asan\n\n"
            "<b>Başlamaq üçün:</b>\n"
            "1️⃣ /start yaz və əsas menyuya qayıt\n"
            "2️⃣ İstədiyin funksiyanı seç\n"
            "3️⃣ Öz Telegram təcrübəni fərqli et!\n\n"
            "<b>Əlaqə və Dəstək:</b>\nSualın varsa, birbaşa adminə yaz: @Rufat19\n\n"
            "Alien_BiBOT — Telegramda rahatlıq, əyləncə və fayda bir arada!"
        )
    }
    return texts.get(key, "")

async def timed_delete(message, delay=20):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception:
        pass

@router.message(F.text == "/info")
async def info_menu(message: Message, state: FSMContext):
    await message.answer(get_text("about_bot_info"), parse_mode="HTML")

@router.callback_query(F.data == "about_bot")
async def about_bot_callback(callback: CallbackQuery, state: FSMContext):
    if callback.message:
        main_menu_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Əsas menyuya qayıt", callback_data="main_menu")]
            ]
        )
        msg = await callback.message.answer(get_text("about_bot_info"), parse_mode="HTML", reply_markup=main_menu_kb)
        asyncio.create_task(timed_delete(msg))
    await callback.answer()
@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery, state: FSMContext):
    if callback.message:
        await callback.message.answer("Aşağıdakı seçimlərdən birini seçin və bütün funksiyalara rahat giriş əldə edin:", reply_markup=get_main_buttons())
    await callback.answer()

@router.callback_query(F.data == "about_channels")
async def about_channels_callback(callback: CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Sosial Mühit", callback_data="channel_sosial_muhit")],
            [InlineKeyboardButton(text="Burada sizin kanalınız ola bilərdi", callback_data="channel_empty1")],
            [InlineKeyboardButton(text="Burada sizin kanalınız ola bilərdi", callback_data="channel_empty2")]
        ]
    )
    if callback.message:
        msg = await callback.message.answer(get_text("about_channels_info"), reply_markup=keyboard)
        asyncio.create_task(timed_delete(msg))
    await callback.answer()

@router.callback_query(F.data == "channel_sosial_muhit")
async def channel_sosial_muhit_callback(callback: CallbackQuery, state: FSMContext):
    if callback.message:
        msg = await callback.message.answer(get_text("channel_sosial_muhit"), parse_mode="HTML")
        asyncio.create_task(timed_delete(msg))
    await callback.answer()

@router.callback_query(F.data == "main_action")
async def main_action_callback(callback: CallbackQuery, state: FSMContext):
    if callback.message is not None:
        await callback.message.answer("🏠 Əsas menyuya qayıtdınız.")
    await callback.answer()

@router.callback_query(F.data == "back")
async def back_callback(callback: CallbackQuery, state: FSMContext):
    if callback.message is not None:
        await callback.message.answer("🏠 Əsas menyuya qayıt:", reply_markup=main_menu_keyboard)
    await callback.answer()