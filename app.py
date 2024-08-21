from flask import Flask, send_from_directory
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создаем экземпляр Flask
app = Flask(__name__)

# Telegram Bot Token
TELEGRAM_TOKEN = '7229780590:AAGhyCEXUeuOyViirGdr3qg5URwX0Sr1aTw'

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я твой Telegram бот.')

# Настройка бота
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))

# Запуск бота в отдельном потоке
updater.start_polling()

# Эндпоинт для отображения GIF
@app.route('/')
def home():
    return send_from_directory('.', 'welcome.gif')

if __name__ == '__main__':
    # Запуск Flask приложения
    app.run(host='0.0.0.0', port=5000)
