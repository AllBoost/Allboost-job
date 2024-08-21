from flask import Flask, send_from_directory
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создаем экземпляр Flask
app = Flask(__name__)

# Telegram Bot Token
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Замените на ваш токен

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я твой Telegram бот.')

# Настройка бота
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Запуск бота в отдельном потоке
application.run_polling()

# Эндпоинт для отображения GIF
@app.route('/')
def home():
    return send_from_directory('.', 'welcome.gif')

if __name__ == '__main__':
    # Запуск Flask приложения
    app.run(host='0.0.0.0', port=5000)
