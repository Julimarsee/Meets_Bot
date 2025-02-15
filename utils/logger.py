import logging
from utils.paths import LOG_FILE

def setup_logging():
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ])

def log_receive_message(msg: str):
    logging.info(f'Message is received: {msg}')