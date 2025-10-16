import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()


# ===================== QUIZ SUALLARI =====================
QUESTIONS = [
    {"q": "2007-ci ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["8.3%", "16.7%", "20.8%", "12.4%"], "answer": 0},
    {"q": "2008-ci ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["20.8%", "16.7%", "11.4%", "3.4%"], "answer": 1},
    {"q": "2009-cu ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["16.7%", "20.8%", "14.7%", "11.2%"], "answer": 1},
    {"q": "2010-cu ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["1.5%", "3%", "5.7%", "7.9%"], "answer": 0},
    {"q": "2011-ci ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["5.7%", "7.9%", "4%", "12.4%"], "answer": 0},
    {"q": "2012-ci ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["1.1%", "7.9%", "2.4%", "4%"], "answer": 1},
    {"q": "2013-cü ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["1.1%", "2.4%", "4.0%", "3%"], "answer": 0},
    {"q": "2014-cü ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["2.4%", "4.0%", "1.4%", "5.7%"], "answer": 0},
    {"q": "2015-ci ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["1.4%", "3%", "4%", "11.2%"], "answer": 0},
    {"q": "2016-cı ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["1.4%", "7.9%", "1.1%", "11.4%"], "answer": 0},
    {"q": "2017-ci ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["12.4%", "5.7%", "7.9%", "3%"], "answer": 0},
    {"q": "2018-ci ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["5.7%", "12.4%", "4%", "3.4%"], "answer": 0},
    {"q": "2019-cu ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["3%", "11.4%", "8.1%", "14.7%"], "answer": 0},
    {"q": "2020-ci ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["16.6%", "11.4%", "14.7%", "3.4%"], "answer": 0},
    {"q": "2021-ci ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["11.4%", "3.4%", "14.7%", "8.1%"], "answer": 0},
    {"q": "2022-ci ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["3.4%", "11.4%", "8.1%", "12.4%"], "answer": 0},
    {"q": "2023-cü ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["14.7%", "11.2%", "8.1%", "3.4%"], "answer": 0},
    {"q": "2024-cü ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["11.2%", "14.7%", "8.1%", "3%"], "answer": 0},
    {"q": "2025-ci ildə pensiyanın sığorta hissəsinin neçə faiz indeksləşdirilərək artırıldı?", "options": ["8.1%", "11.2%", "14.7%", "3.4%"], "answer": 0},
    {"q": "2019-cu ildə istifadə olunmamış kapital neçə faiz indeksləşdirilərək artırıldı?", "options": ["5.01%", "5.29%", "5.14%", "6.43%"], "answer": 0},
    {"q": "2020-ci ildə istifadə olunmamış kapital neçə faiz indeksləşdirilərək artırıldı?", "options": ["5.14%", "5.01%", "5.29%", "6.43%"], "answer": 0},
    {"q": "2021-ci ildə istifadə olunmamış kapital neçə faiz indeksləşdirilərək artırıldı?", "options": ["5.29%", "5.14%", "5.64%", "6.43%"], "answer": 0},
    {"q": "2022-ci ildə istifadə olunmamış kapital neçə faiz indeksləşdirilərək artırıldı?", "options": ["5.64%", "5.29%", "5.14%", "8.8%"], "answer": 0},
    {"q": "2023-cü ildə istifadə olunmamış kapital neçə faiz indeksləşdirilərək artırıldı?", "options": ["6.43%", "5.64%", "5.14%", "2.2%"], "answer": 0},
    {"q": "2024-cü ildə istifadə olunmamış kapital neçə faiz indeksləşdirilərək artırıldı?", "options": ["8.8%", "6.43%", "5.64%", "5.29%"], "answer": 0},
    {"q": "2025-ci ildə istifadə olunmamış kapital neçə faiz indeksləşdirilərək artırıldı?", "options": ["2.2%", "5.01%", "6.43%", "5.64%"], "answer": 0},
     # 🧾 Minimum əməkhaqqı
    {"q": "2022-ci ildə Azərbaycanda minimum əməkhaqqı neçə manat idi?", 
     "options": ["250 manat", "300 manat", "345 manat", "400 manat"], 
     "answer": 1},
    {"q": "2023-cü ildə minimum əməkhaqqı neçə manat müəyyən edilmişdi?", 
     "options": ["300 manat", "345 manat", "375 manat", "400 manat"], 
     "answer": 1},
    {"q": "2025-ci ildən etibarən işçilərin minimum əməkhaqqı neçə manatdan az ola bilməz?", 
     "options": ["345 manat", "370 manat", "400 manat", "420 manat"], 
     "answer": 2},
    # 🌍 Ümumi yaşayış minimumu
    {"q": "2021-ci il üçün ölkə üzrə yaşayış minimumu neçə manat müəyyən edilmişdi?", 
     "options": ["185 manat", "196 manat", "207 manat", "210 manat"], 
     "answer": 1},
    {"q": "2023-cü ildə ölkə üzrə yaşayış minimumu neçə manat idi?", 
     "options": ["210 manat", "220 manat", "246 manat", "270 manat"], 
     "answer": 2},
    {"q": "2025-ci ildə ölkə üzrə yaşayış minimumu neçə manat müəyyən edilib?", 
     "options": ["270 manat", "275 manat", "280 manat", "285 manat"], 
     "answer": 3},
    # 👨‍🏭 Əmək qabiliyyətli əhali üçün
    {"q": "2022-ci ildə əmək qabiliyyətli əhali üçün yaşayış minimumu neçə manat idi?", 
     "options": ["207 manat", "220 manat", "261 manat", "287 manat"], 
     "answer": 1},
    {"q": "2024-cü ildə əmək qabiliyyətli əhali üçün yaşayış minimumu neçə manat müəyyən edilmişdi?", 
     "options": ["261 manat", "270 manat", "287 manat", "305 manat"], 
     "answer": 2},
    {"q": "2025-ci ildə əmək qabiliyyətli əhali üçün yaşayış minimumu neçə manatdır?", 
     "options": ["287 manat", "295 manat", "305 manat", "315 manat"], 
     "answer": 2},
    # 👴 Pensiyaçılar üçün
    {"q": "2021-ci ildə pensiyaçılar üçün yaşayış minimumu neçə manat idi?", 
     "options": ["160 manat", "162 manat", "165 manat", "175 manat"], 
     "answer": 1},
    {"q": "2023-cü ildə pensiyaçılar üçün yaşayış minimumu neçə manat müəyyən edilmişdi?", 
     "options": ["199 manat", "207 manat", "222 manat", "232 manat"], 
     "answer": 0},
    {"q": "2025-ci ildə pensiyaçılar üçün yaşayış minimumu neçə manatdır?", 
     "options": ["222 manat", "230 manat", "232 manat", "240 manat"], 
     "answer": 2},
    # 👶 Uşaqlar üçün
    {"q": "2021-ci ildə uşaqlar üçün yaşayış minimumu neçə manat idi?", 
     "options": ["162 manat", "175 manat", "193 manat", "220 manat"], 
     "answer": 1},
    {"q": "2022-ci ildə uşaqlar üçün yaşayış minimumu neçə manat idi?", 
     "options": ["175 manat", "193 manat", "220 manat", "235 manat"], 
     "answer": 1},
    {"q": "2025-ci ildə uşaqlar üçün yaşayış minimumu neçə manat müəyyən edilmişdir?", 
     "options": ["235 manat", "240 manat", "246 manat", "250 manat"], 
     "answer": 2},
]

FUN_FACTS = [
    "💡 Bilirdinizmi? Azərbaycanda pensiya artımları hər il əvvəlki ilin orta aylıq əməkhaqqı artım tempinə əsasən indeksləşdirilir!",
    "😎 Sosial trivia: Pensiya kartını itirsəniz, DOST mərkəzinə müraciət etsəniz, 10 dəqiqəyə yenisini sifariş edə bilərsiniz!",
    "📊 Əyləncəli fakt: Əmək pensiyası hesablananda hər il üçün fərqli sığorta kapitalı əmsalı tətbiq olunur – bəli, bu bir az riyaziyyat kimidir!",
    "🧠 Sosial fakt: Əgər pensiyaçı işləyirsə, işdən çıxma zamanı və yaxud hər 6 ildən bir sığorta hissəsi yenidən hesablanır və artım baş verir – işləmək həm də pensiyanı artırır!",
    "😂 Sosial zarafat: Ünvanlı yardımda ailə üzvlərini yazmağı unutsan, sistem səni yazacaq – amma kömək etməyəcək!",
    "💬 Fun Fact: DOST Agentliyinin adı təsadüfi deyil — hərfi mənada “Dayanıqlı Operativ Sosial Təminat” deməkdir!",
    "🪙 Maraqlıdır ki, sosial ödənişlərdəki 1% dəyişiklik minlərlə insanın gəlirinə təsir göstərir.",
    "📅 Sosial trivia: 2019-cu ildən bəri pensiya artımları avtomatlaşdırılmış sistemlə hesablanır — insan səhvi sıfır!"
]

BONUS_VALUES = [0]

@router.message(Command("quiz"))
async def start_quiz(message: Message, state: FSMContext):
    if message.chat.type != "private":
        return
    random_questions = random.sample(QUESTIONS, len(QUESTIONS))
    await state.update_data(questions=random_questions, current=0, prev_msg_id=None)
    await send_question(message, state)

async def send_question(message_or_callback, state: FSMContext):
    data = await state.get_data()
    current = data.get("current", 0)
    questions = data.get("questions", [])
    prev_msg_id = data.get("prev_msg_id")

    if prev_msg_id:
        try:
            await message_or_callback.bot.delete_message(message_or_callback.from_user.id, prev_msg_id)
        except:
            pass

    if current >= len(questions):
        await message_or_callback.answer("📊 Test bitdi!")
        await state.clear()
        return

    qdata = questions[current]
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=opt, callback_data=f"ans_{current}_{i}")] for i, opt in enumerate(qdata["options"])]
    )

    msg = await (message_or_callback.answer if isinstance(message_or_callback, Message) else message_or_callback.message.answer)(
            f"❓ {qdata['q']}", reply_markup=kb
        )
    await state.update_data(prev_msg_id=msg.message_id)

@router.callback_query(F.data.startswith("ans_"))
async def answer_handler(callback: CallbackQuery, state: FSMContext):
    # Safely parse callback data: expected format ans_<qnum>_<chosen>
    try:
        parts = callback.data.split("_")
        if len(parts) != 3:
            raise ValueError("invalid callback format")
        _, qnum_s, chosen_s = parts
        qnum = int(qnum_s)
        chosen = int(chosen_s)
    except Exception:
        await callback.answer("Cavab qəbul edilə bilmədi (keçmiş/yanlış məlumat). Testi yenidən başladın.", show_alert=True)
        return

    data = await state.get_data()
    questions = data.get("questions") or []

    # If questions are missing (state cleared or expired), inform user
    if not questions:
        await callback.answer("Suallar tapılmadı və ya test bitib. /quiz ilə yenidən başlayın.", show_alert=True)
        await state.clear()
        return

    # Validate qnum bounds
    if qnum < 0 or qnum >= len(questions):
        await callback.answer("Bu sual artıq etibarsızdır. Testi yenidən başlatmağı yoxlayın.", show_alert=True)
        await state.clear()
        return

    qitem = questions[qnum]
    options = qitem.get("options", [])
    if chosen < 0 or chosen >= len(options):
        await callback.answer("Seçim etibarsızdır.", show_alert=True)
        return

    correct = qitem.get("answer")
    prev_msg_id = data.get("prev_msg_id")

    if chosen == correct:
        await callback.answer(f"✅ Doğru!\n{random.choice(FUN_FACTS)}", show_alert=True)
    else:
        await callback.answer(f"❌ Yanlış!\n{random.choice(FUN_FACTS)}", show_alert=True)

    # Try to delete previous question message (best-effort)
    if prev_msg_id:
        try:
            chat_id = callback.message.chat.id if callback.message else callback.from_user.id
            await callback.bot.delete_message(chat_id, prev_msg_id)
        except Exception:
            pass

    # Advance and send next question
    await state.update_data(current=qnum+1)
    await send_question(callback, state)

# ===================== FAST TEST START =====================
@router.callback_query(F.data == "fast_test_start")
async def fast_test_start_callback(callback: CallbackQuery, state: FSMContext):
    random_questions = random.sample(QUESTIONS, len(QUESTIONS))
    await state.update_data(questions=random_questions, current=0, prev_msg_id=None)
    await send_question(callback, state)