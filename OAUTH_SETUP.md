# 🔐 Настройка OAuth 2.0 для Google Meet Bot

## 📋 Шаг 1: Создание проекта в Google Cloud Console

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект:
   - Нажмите на выпадающий список проектов вверху
   - Выберите "New Project"
   - Введите название: `meet-telegram-bot`
   - Нажмите "Create"

## 📋 Шаг 2: Включение Google Calendar API

1. В левом меню выберите **APIs & Services** → **Library**
2. В поиске введите "Google Calendar API"
3. Выберите "Google Calendar API"
4. Нажмите **Enable**

## 📋 Шаг 3: Настройка OAuth Consent Screen

1. Перейдите в **APIs & Services** → **OAuth consent screen**
2. Выберите **External** (для тестирования)
3. Заполните обязательные поля:
   - **App name**: `Meet Telegram Bot`
   - **User support email**: ваш email
   - **Developer contact information**: ваш email
4. Нажмите **Save and Continue**
5. На странице "Scopes" нажмите **Add or Remove Scopes**
6. Найдите и добавьте следующие scopes:
   - `https://www.googleapis.com/auth/calendar.events`
   - `https://www.googleapis.com/auth/calendar`
7. Нажмите **Update** → **Save and Continue**
8. На странице "Test users" добавьте свой email для тестирования
9. Нажмите **Save and Continue**

## 📋 Шаг 4: Создание OAuth 2.0 Client ID

1. Перейдите в **APIs & Services** → **Credentials**
2. Нажмите **Create Credentials** → **OAuth client ID**
3. Выберите **Web application**
4. Заполните поля:
   - **Name**: `Meet Bot Web Client`
   - **Authorized redirect URIs**: добавьте `http://localhost:8001/auth/google/callback`
5. Нажмите **Create**
6. **ВАЖНО**: Скопируйте Client ID и Client Secret - они понадобятся для настройки

## 📋 Шаг 5: Скачивание credentials файла

1. На странице Credentials найдите созданный OAuth 2.0 Client ID
2. Нажмите на иконку скачивания (download) справа от названия
3. Скачается файл `client_secret_XXXXX.json`
4. Переименуйте его в `client_secrets.json`

## 🔧 Шаг 6: Настройка проекта

Теперь нужно поместить файл `client_secrets.json` в папку `backend/` вашего проекта.

### Структура файла client_secrets.json:
```json
{
  "web": {
    "client_id": "ваш_client_id.apps.googleusercontent.com",
    "project_id": "meet-telegram-bot",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "ваш_client_secret",
    "redirect_uris": [
      "http://localhost:8001/auth/google/callback"
    ]
  }
}
```

## ✅ Проверка настройки

После настройки OAuth credentials вы сможете:
1. Авторизоваться через Google аккаунт
2. Создавать Google Meet ссылки через Calendar API
3. Использовать бота без ограничений service account

## 🚀 Следующие шаги

1. Поместите `client_secrets.json` в папку `backend/`
2. Запустите backend сервер
3. Протестируйте OAuth flow через Telegram бота
4. При необходимости добавьте дополнительных test users в OAuth consent screen

## 🔒 Безопасность

- Никогда не коммитьте `client_secrets.json` в git
- Добавьте файл в `.gitignore`
- В продакшене используйте переменные окружения для хранения credentials 