"""
Обработчик команд для создания Google Meet ссылок с OAuth авторизацией.
"""

import requests
import logging
from telebot import types

logger = logging.getLogger(__name__)

BACKEND_URL = "http://localhost:8001"

def register_meet_handlers(bot):
    """Регистрирует обработчики команд для работы с встречами."""
    
    @bot.message_handler(commands=['create_meet'])
    def handle_create_meet(message):
        """Обработчик команды создания встречи."""
        user_id = str(message.from_user.id)
        
        try:
            # Пробуем создать встречу сразу
            response = requests.post(
                f"{BACKEND_URL}/create-meet-link-oauth",
                params={"user_id": user_id},
                json={
                    "summary": "Встреча из Telegram",
                    "description": "Встреча создана через Telegram бот",
                    "duration_minutes": 60
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    # Встреча создана успешно
                    meeting_url = data.get('meeting_uri')
                    summary = data.get('summary')
                    start_time = data.get('start_time')
                    
                    bot.reply_to(message, 
                        f"✅ Встреча создана!\n\n"
                        f"📝 Название: {summary}\n"
                        f"🕐 Время: {start_time}\n"
                        f"🔗 Ссылка: {meeting_url}\n\n"
                        f"Поделитесь ссылкой с участниками!"
                    )
                    
                elif data.get('auth_required'):
                    # Нужна авторизация
                    show_auth_required(bot, message, user_id)
                else:
                    # Другая ошибка
                    bot.reply_to(message, 
                        f"❌ Ошибка при создании встречи: {data.get('error')}"
                    )
            else:
                bot.reply_to(message, 
                    "❌ Ошибка связи с сервером. Попробуйте позже."
                )
                
        except Exception as e:
            logger.error(f"Error in create_meet handler: {e}")
            bot.reply_to(message, 
                "❌ Произошла ошибка. Попробуйте позже."
            )
    
    @bot.message_handler(commands=['auth_google'])
    def handle_auth_google(message):
        """Обработчик команды авторизации в Google."""
        user_id = str(message.from_user.id)
        show_auth_required(bot, message, user_id)
    
    @bot.message_handler(commands=['auth_status'])
    def handle_auth_status(message):
        """Проверка статуса авторизации."""
        user_id = str(message.from_user.id)
        
        try:
            # Проверяем, авторизован ли пользователь
            response = requests.post(
                f"{BACKEND_URL}/create-meet-link-oauth",
                params={"user_id": user_id},
                json={"summary": "Test", "duration_minutes": 1}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('auth_required'):
                    bot.reply_to(message, 
                        "❌ Вы не авторизованы в Google.\n"
                        "Используйте /auth_google для авторизации."
                    )
                else:
                    bot.reply_to(message, 
                        "✅ Вы авторизованы в Google!\n"
                        "Можете создавать встречи командой /create_meet"
                    )
            else:
                bot.reply_to(message, "❌ Ошибка проверки статуса")
                
        except Exception as e:
            logger.error(f"Error checking auth status: {e}")
            bot.reply_to(message, "❌ Ошибка проверки статуса")


def show_auth_required(bot, message, user_id):
    """Показывает сообщение с требованием авторизации."""
    try:
        # Получаем ссылку для авторизации
        response = requests.get(
            f"{BACKEND_URL}/auth/google",
            params={"user_id": user_id}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                auth_url = data.get('authorization_url')
                
                # Создаем inline кнопку
                markup = types.InlineKeyboardMarkup()
                auth_button = types.InlineKeyboardButton(
                    "🔐 Авторизоваться в Google", 
                    url=auth_url
                )
                markup.add(auth_button)
                
                bot.reply_to(message,
                    "🔐 Для создания Google Meet ссылок нужно авторизоваться.\n\n"
                    "1️⃣ Нажмите кнопку ниже\n"
                    "2️⃣ Войдите в свой Google аккаунт\n"
                    "3️⃣ Разрешите доступ к календарю\n"
                    "4️⃣ Вернитесь в бот и повторите команду\n\n"
                    "⚠️ Авторизация нужна только один раз!",
                    reply_markup=markup
                )
            else:
                bot.reply_to(message, 
                    f"❌ Ошибка получения ссылки авторизации: {data.get('error')}"
                )
        else:
            bot.reply_to(message, 
                "❌ Ошибка связи с сервером авторизации"
            )
            
    except Exception as e:
        logger.error(f"Error showing auth required: {e}")
        bot.reply_to(message, 
            "❌ Ошибка при получении ссылки авторизации"
        ) 