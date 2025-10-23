import asyncio
import os
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, ADMIN_ID, DB_PATH
from utils.logging_config import setup_logging, get_logger
import background_tasks
from handlers import (
    start, fast_test, about, admin, quiz, quiz_world,
    order_bot, cert, balance, payment, review, pdf,
    news_handler, channel_access, misc
)
from handlers.db_utils import init_db
from database.db import create_tables

async def on_startup(bot):
    logger = get_logger(__name__)
    logger.info("Bot started successfully ✅")
    try:
        bot_chat_id = ADMIN_ID
        asyncio.create_task(background_tasks.send_regular_message(bot, bot_chat_id, interval=3600))
        asyncio.create_task(background_tasks.monitor_new_users(bot, bot_chat_id))
        logger.info("Background tasks scheduled")
    except Exception as e:
        logger.exception(f"Failed to start background tasks: {e}")

async def main():
    setup_logging()
    logger = get_logger(__name__)
    logger.info("Program başladı")

    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    init_db()
    create_tables()

    if not BOT_TOKEN:
        logger.critical("BOT_TOKEN is not set!")
        raise ValueError("BOT_TOKEN is not set!")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(fast_test.router)
    dp.include_router(about.router)
    dp.include_router(admin.router)
    dp.include_router(quiz.router)
    dp.include_router(quiz_world.router)
    dp.include_router(order_bot.router)
    dp.include_router(cert.router)
    dp.include_router(balance.router)
    dp.include_router(payment.payment_router)
    dp.include_router(review.router)
    dp.include_router(pdf.router)
    dp.include_router(news_handler.router)
    dp.include_router(channel_access.router)
    dp.include_router(misc.misc_router)

    logger.info("Bot işə düşür...")

    # Aiogram 3.7 üçün startup event belə qeyd olunur:
    dp.startup.register(lambda: on_startup(bot))

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print("🚀 Railway-də bot işə düşür...")
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Botda xəta baş verdi: {e}")
