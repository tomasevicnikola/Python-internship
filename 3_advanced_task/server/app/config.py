import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    DATABASE_PATH = os.path.join(INSTANCE_DIR, "pizza.sqlite3")

    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

    if not ADMIN_TOKEN:
        raise ValueError("ADMIN_TOKEN environment variable is not set.")