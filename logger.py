import logging
from logging.handlers import RotatingFileHandler
import os

# Logs qovluğu
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log faylının yeri
LOG_FILE = os.path.join(LOG_DIR, "bot.log")

# Log formatı
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"

# Log konfiqurasiya
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8"),
        logging.StreamHandler()  # həm fayla, həm terminala yazır
    ]
)

logger = logging.getLogger("GuardianBot")
