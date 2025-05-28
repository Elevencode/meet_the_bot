"""
Main Telegram bot implementation with inline query support.
"""

import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .config import settings
from .services.meet_service import MeetService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher()

# Initialize services
meet_service = MeetService(backend_url=settings.backend_url)


@dp.message(Command("start"))
async def start_command(message: Message):
    """Handle /start command."""
    logger.info(f"Start command from user {message.from_user.id}")
    
    welcome_text = """
🎉 **Google Meet Telegram Bot**

Привет! Я помогу тебе создавать Google Meet ссылки прямо в чатах.

**Как использовать:**
1. В любом чате введи: `@meet_the_bot`
2. Выбери предложение "Создать Google Meet"
3. Готово! Ссылка будет отправлена в чат

**Команды:**
/start - Показать это сообщение
/help - Справка
/create - Создать встречу прямо здесь

**Особенности:**
✅ Работает в любых чатах (личных и групповых)
✅ Мгновенное создание уникальных встреч
✅ Комнаты создаются автоматически при входе
✅ Никаких настроек не требуется

Попробуй прямо сейчас: введи `@meet_the_bot` в любом чате!
    """
    
    await message.answer(welcome_text, parse_mode="Markdown")


@dp.message(Command("help"))
async def help_command(message: Message):
    """Handle /help command."""
    logger.info(f"Help command from user {message.from_user.id}")
    
    help_text = """
❓ **Справка по Google Meet Bot**

**Inline режим (основной способ):**
1. В любом чате введи: `@meet_the_bot`
2. Увидишь предложение "Создать Google Meet"
3. Нажми на него - ссылка отправится в чат

**Прямые команды:**
• `/start` - Приветствие и инструкции
• `/help` - Эта справка  
• `/create` - Создать встречу в личном чате

**Примеры использования:**
• В групповом чате: `@meet_the_bot` → выбрать → готово!
• В личном чате: `/create` или `@meet_the_bot`

**Что происходит:**
1. Бот создает уникальную Google Meet ссылку
2. Любой может перейти по ссылке
3. Google автоматически создает комнату при входе первого участника

**Проблемы?**
Если что-то не работает, попробуйте:
- Проверить интернет соединение
- Повторить команду через несколько секунд
- Написать разработчику: @your_username

Удачных встреч! 🚀
    """
    
    await message.answer(help_text, parse_mode="Markdown")


@dp.message(Command("create"))
async def create_command(message: Message):
    """Handle /create command - create a meeting directly."""
    logger.info(f"Create command from user {message.from_user.id}")
    
    try:
        # Show "typing" status
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        
        # Create meeting
        result = await meet_service.create_meeting()
        
        if result['success']:
            meeting_url = result['meeting_uri']
            meeting_code = result['meeting_code']
            
            response_text = f"""
🎉 **Google Meet создан!**

🔗 **Ссылка:** {meeting_url}

📋 **Код встречи:** `{meeting_code}`

**Как присоединиться:**
• Нажми на ссылку выше
• Или зайди на meet.google.com и введи код: `{meeting_code}`

Комната будет создана автоматически, когда первый участник присоединится к встрече.

**Поделись этой ссылкой с участниками!** ↗️
            """
            
            # Create inline keyboard with the meeting link
            keyboard = InlineKeyboardBuilder()
            keyboard.button(text="🚀 Присоединиться к встрече", url=meeting_url)
            keyboard.button(text="📋 Копировать код", callback_data=f"copy_code:{meeting_code}")
            keyboard.adjust(1)  # 1 button per row
            
            await message.answer(
                response_text, 
                parse_mode="Markdown",
                reply_markup=keyboard.as_markup(),
                disable_web_page_preview=True
            )
            
        else:
            await message.answer(
                "❌ Произошла ошибка при создании встречи. Попробуйте еще раз через несколько секунд.",
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Error in create command: {e}")
        await message.answer(
            "❌ Произошла ошибка. Попробуйте еще раз позже.",
            parse_mode="Markdown"
        )


@dp.inline_query()
async def inline_query_handler(inline_query: InlineQuery):
    """Handle inline queries - main bot functionality."""
    logger.info(f"Inline query from user {inline_query.from_user.id}: '{inline_query.query}'")
    
    try:
        # Create meeting
        result = await meet_service.create_meeting()
        
        if result['success']:
            meeting_url = result['meeting_uri']
            meeting_code = result['meeting_code']
            
            # Create inline result
            result_item = InlineQueryResultArticle(
                id="create_meet",
                title="🎉 Создать Google Meet",
                description="Создать новую встречу и поделиться ссылкой",
                thumbnail_url="https://fonts.gstatic.com/s/i/productlogos/meet_2020q4/v6/web-512dp/logo_meet_2020q4_color_2x_web_512dp.png",
                input_message_content=InputTextMessageContent(
                    message_text=f"""🎉 **Google Meet создан!**

🔗 **Ссылка:** {meeting_url}

📋 **Код встречи:** `{meeting_code}`

Комната будет создана автоматически при входе первого участника. Присоединяйтесь! 🚀""",
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )
            )
            
            # Answer the inline query
            await inline_query.answer(
                results=[result_item],
                cache_time=1,  # Don't cache results
                is_personal=True
            )
            
        else:
            # Error creating meeting
            error_result = InlineQueryResultArticle(
                id="error",
                title="❌ Ошибка",
                description="Не удалось создать встречу. Попробуйте еще раз.",
                input_message_content=InputTextMessageContent(
                    message_text="❌ Произошла ошибка при создании Google Meet. Попробуйте еще раз.",
                    parse_mode="Markdown"
                )
            )
            
            await inline_query.answer(
                results=[error_result],
                cache_time=1,
                is_personal=True
            )
            
    except Exception as e:
        logger.error(f"Error in inline query handler: {e}")
        
        # Fallback error result
        error_result = InlineQueryResultArticle(
            id="error",
            title="❌ Ошибка",
            description="Произошла техническая ошибка",
            input_message_content=InputTextMessageContent(
                message_text="❌ Произошла техническая ошибка. Попробуйте позже.",
                parse_mode="Markdown"
            )
        )
        
        await inline_query.answer(
            results=[error_result],
            cache_time=1,
            is_personal=True
        )


async def main():
    """Start the bot."""
    logger.info("Starting Google Meet Telegram Bot...")
    logger.info(f"Backend URL: {settings.backend_url}")
    
    try:
        # Test backend connection
        backend_status = await meet_service.test_backend()
        if backend_status:
            logger.info("✅ Backend connection successful")
        else:
            logger.warning("⚠️ Backend connection failed, but starting bot anyway")
        
        # Start bot
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise 