from handlers.channel_access import router as channel_access_router
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.about import router as about_router
from handlers.admin import router as admin_router
from handlers.quiz import router as quiz_router
from handlers.cert import router as cert_router
from handlers.balance import router as balance_router
from handlers.payment import payment_router
from handlers.review import router as review_router
from handlers.game import router as game_router 
from handlers import misc
from handlers.fast_test import router as fast_test_router
from handlers.db_utils import init_db
from database.db import create_tables

async def main():
    print("Program başladı")
    print("main() başladı")
    print("Bot yaradılır...")
    init_db()  # DB-ni initialize et
    create_tables()
    if BOT_TOKEN is None:
        raise ValueError("BOT_TOKEN is not set. Please provide a valid token in config.py.")
    bot = Bot(token=BOT_TOKEN)
    print("Dispatcher yaradılır...")
    dp = Dispatcher()
    print("Router-lar əlavə olunur...")
    dp.include_router(start_router)
    dp.include_router(fast_test_router)
    # dp.include_router(entry_router)
    dp.include_router(about_router)
    dp.include_router(admin_router)
    from handlers.quiz_world import router as quiz_world_router
    from handlers.order_bot import router as order_bot_router
    from handlers.pdf import router as pdf_router
    dp.include_router(quiz_router)
    dp.include_router(quiz_world_router)
    dp.include_router(order_bot_router)
    dp.include_router(cert_router)
    dp.include_router(balance_router)
    dp.include_router(payment_router)
    dp.include_router(review_router)
    dp.include_router(game_router)
    dp.include_router(pdf_router)
    dp.include_router(misc.misc_router)
    dp.include_router(channel_access_router)
    # from handlers.feedback import router as feedback_router
    # dp.include_router(feedback_router)
    print("Bot işə düşür...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


