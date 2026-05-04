import random
import time
import logging
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for professional terminal output
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

class Logger:
    @staticmethod
    def info(message):
        print(f"{Fore.CYAN}[INFO] {datetime.now().strftime('%H:%M:%S')} - {message}")
        logging.info(message)

    @staticmethod
    def success(message):
        print(f"{Fore.GREEN}[SUCCESS] {datetime.now().strftime('%H:%M:%S')} - {message}")
        logging.info(message)

    @staticmethod
    def error(message):
        print(f"{Fore.RED}[ERROR] {datetime.now().strftime('%H:%M:%S')} - {message}")
        logging.error(message)

    @staticmethod
    def warn(message):
        print(f"{Fore.YELLOW}[WARN] {datetime.now().strftime('%H:%M:%S')} - {message}")
        logging.warning(message)

def get_random_user_agent():
    """Returns a realistic mobile User-Agent string."""
    mobile_uas = [
        "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.036; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36"
    ]
    return random.choice(mobile_uas)

def human_delay(min_sec=3, max_sec=8):
    """Introduces a random delay with slight jitter to mimic human behavior."""
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)

def get_headers(cookies_dict=None):
    """Generates standard professional headers for mbasic.facebook.com."""
    headers = {
        'authority': 'mbasic.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'dpr': '1',
        'sec-ch-prefers-color-scheme': 'dark',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
        'sec-ch-ua-full-version-list': '"Not:A-Brand";v="99.0.0.0", "Chromium";v="112.0.5615.137"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-model': '"SM-S901B"',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua-platform-version': '"13.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': get_random_user_agent(),
    }
    return headers
