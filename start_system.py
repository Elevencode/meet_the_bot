#!/usr/bin/env python3
"""
Скрипт для запуска всей системы Google Meet Bot.
Запускает backend сервер и Telegram бота одновременно.
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path

def run_backend():
    """Запуск backend сервера."""
    print("🚀 Запуск backend сервера...")
    backend_dir = Path(__file__).parent / "backend"
    
    try:
        # Переходим в директорию backend
        os.chdir(backend_dir)
        
        # Запускаем uvicorn сервер
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8001", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("🛑 Backend сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка запуска backend: {e}")

def run_bot():
    """Запуск Telegram бота."""
    print("🤖 Запуск Telegram бота...")
    bot_dir = Path(__file__).parent / "bot"
    
    # Ждем запуска backend
    time.sleep(3)
    
    try:
        # Переходим в директорию bot
        os.chdir(bot_dir)
        
        # Запускаем бота
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("🛑 Telegram бот остановлен")
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")

def signal_handler(signum, frame):
    """Обработчик сигналов для корректного завершения."""
    print("\n🛑 Получен сигнал завершения. Останавливаем систему...")
    sys.exit(0)

def main():
    """Основная функция запуска системы."""
    print("🚀 Запуск Google Meet Bot System")
    print("=" * 50)
    
    # Проверяем наличие необходимых файлов
    backend_dir = Path(__file__).parent / "backend"
    bot_dir = Path(__file__).parent / "bot"
    
    if not backend_dir.exists():
        print("❌ Директория backend не найдена")
        return
    
    if not bot_dir.exists():
        print("❌ Директория bot не найдена")
        return
    
    # Проверяем наличие client_secrets.json
    client_secrets = backend_dir / "client_secrets.json"
    if not client_secrets.exists():
        print("❌ Файл client_secrets.json не найден в backend/")
        print("📋 Пожалуйста, следуйте инструкциям в OAUTH_SETUP.md")
        return
    
    # Проверяем переменную окружения BOT_TOKEN
    if not os.getenv('BOT_TOKEN'):
        print("❌ Переменная окружения BOT_TOKEN не установлена")
        print("📋 Установите токен бота: export BOT_TOKEN=your_token_here")
        return
    
    # Устанавливаем обработчик сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Запускаем backend в отдельном потоке
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Запускаем бота в основном потоке
        run_bot()
        
    except KeyboardInterrupt:
        print("\n🛑 Система остановлена пользователем")
    except Exception as e:
        print(f"❌ Ошибка системы: {e}")
    finally:
        print("👋 Завершение работы системы")

if __name__ == "__main__":
    main() 