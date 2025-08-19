import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()


# ===================== QUIZ SUALLARI =====================
QUESTIONS = [
    {"q": "Which file format is most commonly used for storing structured data in Data Science?", "options": ["JPG", "PDF", "CVS", "HTML"], "answer": 2},
    {"q": "Which protocol is secure for web browsing?", "options": ["http", "https", "SNMP", "FTP"], "answer": 1},
    {"q": "What does Excel Copilot use for contextual understanding?", "options": ["Macros", "NLP", "Rules", "Tables"], "answer": 0},
    {"q": "Which of the following is NOT a type of malware?", "options": ["Worm", "Phishing", "Trojan", "Ransomware"], "answer": 1},
    {"q": "What’s the most common cause of security breaches?", "options": ["Weak passwords", "Unpatched software", "Insider threats", "Phishing attacks"], "answer": 3},
    {"q": "What can be used to automatically fill patterns?", "options": ["Custom Sort", "Data validation", "Fill Handle", "Flash Fill"], "answer": 3},
    {"q": "Which Data Science technique helps identify patterns in large datasets?", "options": ["Splitting", "Mining", "Looping", "Fitting"], "answer": 1},
    {"q": "Which tool allows you to solve equations or optimize values in Excel?", "options": ["Flash Fill", "Solver", "Data Table", "Scenario Manager"], "answer": 1},
    {"q": "𝗪𝗵𝗮𝘁 𝗱𝗼𝗲𝘀 𝗮 𝗱𝗮𝘁𝗮𝗯𝗮𝘀𝗲 𝗮𝗰𝘁𝘂𝗮𝗹𝗹𝘆 𝘀𝘁𝗼𝗿𝗲?", "options": ["Queries", "Tables", "Files", "Data"], "answer": 3},
    {"q": "Which feature splits full names into first and last?", "options": ["Filter", "Flash Fill", "CONCAT", "Solver"], "answer": 1},
    {"q": "In SQL, which clause is evaluated first in a SELECT statement ?", "options": ["Select", "From", "Group By", "Where"], "answer": 1},
    {"q": "What does Power Query allow analytics to do in Excel?", "options": ["Create charts", "Write VBA macros", "Transform & clean data", "Record keyboard shortcuts"], "answer": 2},
    {"q": "What type of variable is “Customer Gender”?", "options": ["Numerical", "Interval", "Categorical", "Ordinal"], "answer": 2},
    {"q": "What is the output of: print(3 ** 3)?", "options": ["27", "243", "81", "9"], "answer": 0},
    {"q": "Which standard defines requirements for information security management systems?", "options": ["SOC 2", "HIPAA", "ISO 27001", "GPDR"], "answer": 2},
    {"q": "which port is commonly used for HTTPS communication", "options": ["443", "22", "80", "21"], "answer": 0},
    {"q": "What will be the output of the following Python code? def status(): print(flag) flag = True status()", "options": ["Error", "True", "status", "False"], "answer": 1},
    {"q": "Which type of malware is designed to replicate itself and spread?", "options": ["Spyware", "Ransomware", "Trojan", "Worm"], "answer": 3},
    {"q": "Which of the following is a data type in Python?", "options": ["String", "Field", "Table", "Sheet"], "answer": 0},
    {"q": "What does the type() function return in Python?", "options": ["value", "class", "string", "object"], "answer": 1},
    {"q": "Which of the following tools helps restrict data input in a cell?", "options": ["Conditional Formatting", "Goal Seek", "Data Validation", "Conditional Formatting"], "answer": 2},
    {"q": "What does the “Flash Fill” feature do in Excel?", "options": ["Deletes blank cells", "Sorts a list automatically", "Fills values base on a pattern", "Merges two columns"], "answer": 2},
    {"q": "What tool prevents duplicate entry?", "options": ["Data Bars", "Data Validation", "Goal Seek", "Flash Fill"], "answer": 1},
    {"q": "Which of the following is a social engineering technique?", "options": ["Man-in-the-middle attack", "Sql injection", "Phishing", "Brute-force attack"], "answer": 2},
    {"q": "In SQL, which function is used to concatenate two strings?", "options": ["APPEND", "CONCAT", "JOİN", "MERGE"], "answer": 1},
    {"q": "Which term defines the acceptable downtime for a system?", "options": ["RPO", "RTO", "MTD", "SLA"], "answer": 1},
    {"q": "What does =A1&' '&B1 do?", "options": ["Returns blank", "Multiplies cells", "Adds values", "Joins with space"], "answer": 3},
    {"q": "What will be the output of the following Python code? def add_five(n): n += 5 value = 10 add_five(value) print(value)", "options": ["15", "5", "Error", "10"], "answer": 0},
    {"q": "Which function finds a value by row and column?", "options": ["MATCH", "VLOOKUP", "OFFSET", "INDEX"], "answer": 1},
    {"q": "Which Excel feature allows you to restrict user input in a cell?", "options": ["Filters", "Goal Seek", "Conditional Formatting", "Data Validation"], "answer": 3},
    {"q": "Which function can be used to count cells based on a condition?", "options": ["LET", "COUNTİF", "İF", "SUM"], "answer": 1},
    {"q": "What kind of attack floods a system with traffic to overload resources?", "options": ["SQL Injection", "Man-in-the-middle", "DDoS Attack", "Keylogging"], "answer": 2},
    {"q": "Which port does SNMP use?", "options": ["25", "143", "443", "161"], "answer": 3},
    {"q": "Which function returns a table with a single column of all dates between a start and end date?", "options": ["CALENDAR()", "DATESBETWEEN()", "DATEVALUE()", "EDATE()"], "answer": 1},
    {"q": "What kind of attack involves tricking users into revealing confidential information?", "options": ["Social engineering", "Phishing", "Brute force", "DDoS"], "answer": 0},
    {"q": "What is a bug bounty program?", "options": ["Sell bugs", "Find & report bugs", "Delete malware", "Hire hackers"], "answer": 1},
    {"q": "Which function returns the number of working days between two dates?", "options": ["WORKDAY", "DAYS", "NETWORKDAYS", "DATEDIF"], "answer": 2},
    {"q": "Which AI-powered feature replaces manual insights discovery?", "options": ["Power View", "Power Map", "Analyze Data", "Goal Seek"], "answer": 2},
    {"q": "What’s the advantage of XLOOKUP over VLOOKUP?", "options": ["It only works with tables", "Supports vertical lookup only", "Can return multi colms at once", "It works only with ranges"], "answer": 2},
    {"q": "What does VLOOKUP default to if the last argument (range_lookup) is omitted?", "options": ["FALSE (exact match)", "It throws an error", "#N/A", "TRUE (approximate match)"], "answer": 3},
    {"q": "Which algorithm is commonly used for clustering?", "options": ["Decision Tree", "K-Means", "Random Forest", "Linear Regression"], "answer": 1},
    {"q": "What is DSE (Driver Signature Enforcement) in Windows?", "options": ["Dynamic shell escape", "DNS sinkhole engine", "Driver signature check", "Disk sector erasure"], "answer": 2},
    {"q": "Which Microsoft Azure tool works like a SIEM?", "options": ["Azure Key Vault", "Azure Sentinel", "Azure Firewall", "Azure Defender"], "answer": 0},
    {"q": "Which SQL clause is used to filter records?", "options": ["ORDER BY", "FILTER", "SELECT", "WHERE"], "answer": 3},
    {"q": "What is the default sorting order in ORDER BY?", "options": ["DESC", "ASC", "RANDOM", "None"], "answer": 1},
    {"q": "Which function adds up values based on a single condition?", "options": ["SUMIFS", "SUMIF", "COUNTIF", "ADDIF"], "answer": 1},
    {"q": "What is required to access AI Copilot in Excel?", "options": ["Office 2021", "Excel Online", "M365 subscription", "Windows 7"], "answer": 2},
    {"q": "What is the purpose of 'Calculated Field' in PivotTable?", "options": ["Perform calc. outside PvtTable", "+custom formulas in PivotTable", "Adds a new worksheet", "Deletes a column"], "answer": 1},
    {"q": "In Excel, which keyboard shortcut is used to create a new worksheet?", "options": ["Ctrl + N", "Shift + F11", "Alt + N", "Ctrl + W"], "answer": 0},
    {"q": "Which SQL constraint ensures a column cannot have NULL values?", "options": ["UNIQUE", "INDEX", "NOTNULL", "CHECK"], "answer": 2},
]

FUN_FACTS = [
    "💡 Fun Fact: Excel-də Ctrl + Z ilə səhvləri düzəldə bilərsiniz!",
    "😂 Trivia: Python yılan deyil, proqramlaşdırma dili!",
    "😎 Hint: VLOOKUP-un gücü gözlə görünmür, amma möcüzədir.",
    "📊 Data Science = Magiya? Yox, yalnız statistika!"
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
    _, qnum, chosen = callback.data.split("_")
    qnum = int(qnum)
    chosen = int(chosen)
    data = await state.get_data()
    questions = data.get("questions", [])
    correct = questions[qnum]["answer"]
    prev_msg_id = data.get("prev_msg_id")
    if chosen == correct:
        await callback.answer(f"✅ Doğru! 🎉\n{random.choice(FUN_FACTS)}", show_alert=True)
    else:
        await callback.answer(f"❌ Yanlış! 😅\n{random.choice(FUN_FACTS)}", show_alert=True)
    if prev_msg_id:
        try:
            await callback.bot.delete_message(callback.from_user.id, prev_msg_id)
        except:
            pass
    await state.update_data(current=qnum+1)
    await send_question(callback, state)

# ===================== FAST TEST START =====================
@router.callback_query(F.data == "fast_test_start")
async def fast_test_start_callback(callback: CallbackQuery, state: FSMContext):
    random_questions = random.sample(QUESTIONS, len(QUESTIONS))
    await state.update_data(questions=random_questions, current=0, prev_msg_id=None)
    await send_question(callback, state)
