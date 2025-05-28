#!/usr/bin/env python3
"""
Основной файл Telegram бота для создания Google Meet ссылок.
Интегрирован с OAuth 2.0 для авторизации пользователей.
"""

import os
import logging
import telebot
from telebot import types
from handlers.meet_handler import register_meet_handlers

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Токен бота (получите у @BotFather)
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
    logger.error("Пожалуйста, установите BOT_TOKEN в переменных окружения")
    exit(1)

# Создание экземпляра бота
bot = telebot.TeleBot(BOT_TOKEN)

# Регистрация обработчиков
register_meet_handlers(bot)

@bot.message_handler(commands=['start'])
def handle_start(message):
    """Обработчик команды /start."""
    welcome_text = """
🤖 Добро пожаловать в Google Meet Bot!

Этот бот поможет вам создавать ссылки на Google Meet встречи.

📋 Доступные команды:
• /create_meet - Создать новую встречу
• /auth_google - Авторизоваться в Google
• /auth_status - Проверить статус авторизации
• /help - Показать справку

🔐 Для работы бота необходимо авторизоваться в Google аккаунте.
Используйте команду /auth_google для начала авторизации.

⚡ Быстрый старт:
1. Нажмите /auth_google
2. Авторизуйтесь в браузере
3. Вернитесь в бот и используйте /create_meet
"""
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['help'])
def handle_help(message):
    """Обработчик команды /help."""
    help_text = """
📖 Справка по Google Meet Bot

🔧 Команды:
• /start - Приветствие и инструкции
• /create_meet - Создать Google Meet встречу
• /auth_google - Авторизация в Google
• /auth_status - Проверить авторизацию
• /help - Эта справка

🔐 Авторизация:
Для создания встреч нужно авторизоваться в Google:
1. Используйте /auth_google
2. Перейдите по ссылке в браузере
3. Войдите в Google аккаунт
4. Разрешите доступ к календарю
5. Вернитесь в бот

✨ Создание встреч:
После авторизации используйте /create_meet для создания новой встречи.
Бот автоматически создаст событие в календаре с Google Meet ссылкой.

❓ Проблемы:
• Если авторизация не работает - попробуйте /auth_google снова
• Если встреча не создается - проверьте /auth_status
• При других проблемах обратитесь к администратору

🔒 Безопасность:
Бот использует OAuth 2.0 для безопасной авторизации.
Ваши данные защищены и не сохраняются на сервере.
"""
    bot.reply_to(message, help_text)

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    """Обработчик неизвестных команд."""
    unknown_text = """
❓ Неизвестная команда.

Используйте /help для просмотра доступных команд.

Основные команды:
• /create_meet - Создать встречу
• /auth_google - Авторизация
• /help - Справка
"""
    bot.reply_to(message, unknown_text)

def main():
    """Основная функция запуска бота."""
    logger.info("🚀 Запуск Google Meet Bot...")
    
    try:
        # Проверка подключения к backend
        import requests
        backend_url = "http://localhost:8001"
        
        try:
            response = requests.get(f"{backend_url}/ping", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Backend сервер доступен")
            else:
                logger.warning("⚠️ Backend сервер отвечает с ошибкой")
        except requests.exceptions.RequestException:
            logger.error("❌ Backend сервер недоступен. Убедитесь, что сервер запущен на localhost:8001")
            
        # Запуск бота
        logger.info("🤖 Бот запущен и готов к работе!")
        bot.infinity_polling(none_stop=True)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    main() 