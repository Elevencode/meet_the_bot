from pydantic_settings import BaseSettings
from typing import Optional
import os

class TestSettings(BaseSettings):
    google_service_account_path: Optional[str] = None
    telegram_bot_token: Optional[str] = None # Добавим еще одну для проверки

    class Config:
        env_file = ".env" # Ищем .env в текущей директории
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

# Получаем текущую рабочую директорию
cwd = os.getcwd()
print(f"Current working directory: {cwd}")

# Проверяем существование .env файла
dotenv_path = os.path.join(cwd, ".env")
print(f"Expected .env path: {dotenv_path}")
print(f".env file exists: {os.path.exists(dotenv_path)}")

if os.path.exists(dotenv_path):
    print("---- .env content ----")
    with open(dotenv_path, "r") as f:
        print(f.read())
    print("----------------------")

try:
    settings = TestSettings()
    print(f"Loaded GOOGLE_SERVICE_ACCOUNT_PATH: '{settings.google_service_account_path}'")
    print(f"Loaded TELEGRAM_BOT_TOKEN: '{settings.telegram_bot_token}'")
except Exception as e:
    print(f"Error loading settings: {e}") 