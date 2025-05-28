# 🤖 Google Meet Telegram Bot

Telegram бот для создания Google Meet ссылок с использованием OAuth 2.0 авторизации.

## 🚀 Возможности

- ✅ Создание Google Meet ссылок через Telegram
- ✅ OAuth 2.0 авторизация (работает с бесплатными Google аккаунтами)
- ✅ Красивый пользовательский интерфейс
- ✅ Автоматическое управление календарными событиями
- ✅ Безопасное хранение токенов авторизации

## 📋 Требования

- Python 3.8+
- Google аккаунт
- Telegram бот токен

## 🛠 Установка

### 1. Клонирование и установка зависимостей

```bash
# Установка зависимостей для backend
cd backend
pip install -r requirements.txt

# Установка зависимостей для бота
cd ../bot
pip install -r requirements.txt
```

### 2. Настройка Google OAuth 2.0

Следуйте подробным инструкциям в файле `OAUTH_SETUP.md`:

1. Создайте проект в Google Cloud Console
2. Включите Google Calendar API
3. Настройте OAuth Consent Screen
4. Создайте OAuth 2.0 Client ID
5. Скачайте `client_secrets.json` в папку `backend/`

### 3. Создание Telegram бота

1. Напишите [@BotFather](https://t.me/BotFather) в Telegram
2. Создайте нового бота командой `/newbot`
3. Получите токен бота
4. Установите переменную окружения:

```bash
export BOT_TOKEN=your_telegram_bot_token_here
```

### 4. Настройка переменных окружения

Скопируйте пример файла и настройте переменные:

```bash
# В директории bot/
cp env_example.txt .env
# Отредактируйте .env файл с вашими данными
```

## 🚀 Запуск

### Автоматический запуск (рекомендуется)

```bash
python start_system.py
```

Этот скрипт автоматически запустит backend сервер и Telegram бота.

### Ручной запуск

#### Backend сервер:
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

#### Telegram бот:
```bash
cd bot
python main.py
```

## 📱 Использование

1. **Запустите бота** командой `/start`
2. **Авторизуйтесь** командой `/auth_google`
   - Бот отправит ссылку для авторизации в Google
   - Перейдите по ссылке и разрешите доступ
   - Вернитесь в бота после успешной авторизации
3. **Создайте встречу** командой `/create_meet`
   - Введите название встречи
   - Получите ссылку на Google Meet

### Доступные команды

- `/start` - Приветствие и инструкции
- `/help` - Справка по командам
- `/auth_google` - Авторизация в Google аккаунте
- `/create_meet` - Создание новой встречи
- `/status` - Проверка статуса авторизации

## 🏗 Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram      │    │   Backend       │    │   Google        │
│   Bot           │◄──►│   FastAPI       │◄──►│   Calendar API  │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Компоненты:

- **Backend (FastAPI)**: REST API для работы с Google Calendar API
- **Bot (pyTelegramBotAPI)**: Telegram бот интерфейс
- **OAuth 2.0**: Безопасная авторизация пользователей

## 📁 Структура проекта

```
meet_the_bot/
├── backend/                 # Backend сервер
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py   # API endpoints
│   │   ├── services/
│   │   │   └── meet_service.py
│   │   ├── config.py       # Конфигурация
│   │   └── main.py         # FastAPI приложение
│   ├── client_secrets.json # OAuth credentials
│   └── requirements.txt
├── bot/                    # Telegram бот
│   ├── handlers/
│   │   └── meet_handler.py # Обработчики команд
│   ├── main.py            # Основной файл бота
│   ├── requirements.txt
│   └── env_example.txt    # Пример переменных окружения
├── start_system.py        # Скрипт запуска системы
├── OAUTH_SETUP.md         # Инструкции по настройке OAuth
└── README.md              # Этот файл
```

## 🔧 Разработка

### Тестирование backend

```bash
cd backend
# Проверка работы сервера
curl http://localhost:8001/ping

# Проверка OAuth endpoints
curl http://localhost:8001/auth/google?user_id=test_user
```

### Логирование

Все компоненты системы ведут подробные логи:
- Backend: логи FastAPI и Google API
- Bot: логи Telegram API и пользовательских действий

## 🔒 Безопасность

- OAuth 2.0 токены хранятся в памяти (не в файлах)
- Поддержка refresh токенов для длительной работы
- Валидация всех входящих данных
- Безопасная обработка ошибок

## 🐛 Устранение неполадок

### Частые проблемы:

1. **"Invalid conference type value"**
   - Убедитесь, что используете OAuth 2.0 (не service account)
   - Проверьте права доступа в Google Cloud Console

2. **"BOT_TOKEN not found"**
   - Установите переменную окружения: `export BOT_TOKEN=your_token`

3. **"client_secrets.json not found"**
   - Скачайте файл из Google Cloud Console в папку `backend/`

4. **Бот не отвечает**
   - Проверьте, что backend сервер запущен на порту 8001
   - Проверьте логи бота на наличие ошибок

### Проверка статуса:

```bash
# Проверка backend
curl http://localhost:8001/ping

# Проверка переменных окружения
echo $BOT_TOKEN
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи backend и бота
2. Убедитесь, что все зависимости установлены
3. Проверьте настройки OAuth в Google Cloud Console
4. Убедитесь, что все переменные окружения установлены

## 📄 Лицензия

MIT License - используйте свободно для личных и коммерческих проектов.

---

**Создано с ❤️ для удобного создания Google Meet ссылок через Telegram** 