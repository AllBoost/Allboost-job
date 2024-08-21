from flask import Flask, request
from telegram import Bot
from telegram.ext import CommandHandler, Dispatcher
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создание экземпляра Flask
app = Flask(__name__)

# Ваш токен бота
TOKEN = '7229780590:AAGhyCEXUeuOyViirGdr3qg5URwX0Sr1aTw'
bot = Bot(token=TOKEN)

# Функция для обработки команды /start
def start(update, context):
    chat_id = update.effective_chat.id
    # Отправка GIF-файла
    try:
        with open('welcome.gif', 'rb') as gif:
            bot.send_animation(chat_id, gif)
    except Exception as e:
        logging.error(f"Ошибка при отправке GIF: {e}")

# Настройка диспетчера
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))

# Эндпоинт для получения обновлений от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    try:
        dispatcher.process_update(update)
    except Exception as e:
        logging.error(f"Ошибка при обработке обновления: {e}")
    return '', 200

# Запуск веб-приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Убедитесь, что Flask слушает на всех интерфейсах
