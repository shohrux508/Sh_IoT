import os
import ssl

from dotenv import load_dotenv
import logging

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError('Database URL not given!')

ssl_context = ssl.create_default_context()

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
