import asyncio
import os
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, ADMIN_ID, DB_PATH
from utils.logging_config import setup_logging, get_logger
import background_tasks

# --- Handlers importları ---
from handlers.start import router as start_router
from handlers.fast_test import router as fast_test_router
from handlers.about import router as about_router
from handlers.admin import router as admin_router
from handlers.quiz import router as quiz_router
from handlers.quiz_world import router as quiz_world_router
from handlers.order_bot import router as order_bot_router
from handlers.cert import router as cert_router
from handlers.balance import router as balance_router
from handlers.payment import payment_router
from handlers.review import router as review_router
from handlers.pdf import router as pdf_router
from handlers.news_handler import router as news_router
from handlers.channel_access import router as channel_access_router
from handlers import misc
from handlers.db_utils import init_db
from database.db import create_tables

async def main():
    # Logger
    setup_logging()
    logger = get_logger(__name__)
    logger.info("Program başladı")
    logger.debug("main() başladı")
    
    # Ensure database directory exists
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    
    # Database initialization
    init_db()
    create_tables()
    
    # Token yoxlaması
    if not BOT_TOKEN:
        logger.critical("BOT_TOKEN is not set!")
        raise ValueError("BOT_TOKEN is not set!")
    
    # Bot və Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Router-lar əlavə olunur
    logger.info("Router-lar əlavə olunur...")
    dp.include_router(start_router)
    dp.include_router(fast_test_router)
    dp.include_router(about_router)
    dp.include_router(admin_router)
    dp.include_router(quiz_router)
    dp.include_router(quiz_world_router)
    dp.include_router(order_bot_router)
    dp.include_router(cert_router)
    dp.include_router(balance_router)
    dp.include_router(payment_router)
    dp.include_router(review_router)
    dp.include_router(pdf_router)
    dp.include_router(news_router)
    dp.include_router(channel_access_router)
    dp.include_router(misc.misc_router)
    
    logger.info("Bot işə düşür...")

    # Startup handler → background tasks
    @dp.startup()
    async def on_startup():
        logger.info("Bot started successfully ✅")
        try:
            bot_chat_id = ADMIN_ID
            # Background tasks
            asyncio.create_task(background_tasks.send_regular_message(bot, bot_chat_id, interval=3600))
            asyncio.create_task(background_tasks.monitor_new_users(bot, bot_chat_id))
            logger.info("Background tasks scheduled")
        except Exception as e:
            logger.exception(f"Failed to start background tasks: {e}")
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
