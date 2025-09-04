import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "app_data.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"
