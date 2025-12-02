import os

from dotenv import load_dotenv

load_dotenv()
APP_TITLE = os.getenv("APP_TITLE", "Personal Finance App")
PAGES_PATH = "src/pages"
