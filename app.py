import json
import pandas as pd
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Загрузка и сохранение пользователей
def load_users():
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def add_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)

# Функция для записи пользователя в Excel с добавлением номера телефона и даты регистрации
def add_user_to_excel(username: str, user_id: int, phone_number: str = '', registration_date: str = ''):
    user_id = str(user_id)  # Преобразуем ID пользователя в строку
    phone_number = str(phone_number)  # Преобразуем номер телефона в строку

    try:
        df = pd.read_excel('Пользователи.xlsx', sheet_name='Sheet1')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Имя пользователя", "ID", "номер телефона", "Дата регистрации"])

    # Приводим столбец "номер телефона" к строковому типу данных, если он существует
    if 'номер телефона' in df.columns:
        df['номер телефона'] = df['номер телефона'].astype(str)

    # Проверяем, существуют ли необходимые столбцы
    if 'ID' not in df.columns:
        df['ID'] = ''
    if 'номер телефона' not in df.columns:
        df['номер телефона'] = ''
    if 'Дата регистрации' not in df.columns:
        df['Дата регистрации'] = ''

    # Проверяем, существует ли пользователь
    if user_id not in df['ID'].astype(str).values:
        if not registration_date:
            registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_user = pd.DataFrame([[username, user_id, phone_number, registration_date]], 
                                columns=["Имя пользователя", "ID", "номер телефона", "Дата регистрации"])
        df = pd.concat([df, new_user], ignore_index=True)
    else:
        # Обновляем номер телефона и дату регистрации, если они отсутствуют
        if phone_number:
            df.loc[df['ID'].astype(str) == user_id, 'номер телефона'] = phone_number
        if registration_date:
            df.loc[df['ID'].astype(str) == user_id, 'Дата регистрации'] = registration_date

    # Сохраняем обновленные данные обратно в файл
    df.to_excel('Пользователи.xlsx', sheet_name='Sheet1', index=False)

# Новая функция для получения данных из файла "Рабочая информация.xlsx"
def get_work_info(user_id: str):
    try:
        df = pd.read_excel('Рабочая информация.xlsx', sheet_name='Sheet1')
    except FileNotFoundError:
        return None

    if user_id in df['ID'].astype(str).values:
        user_data = df.loc[df['ID'].astype(str) == user_id].iloc[0]

        # Вычисляем "Плановую дату выполнения", если она отсутствует
        if pd.isna(user_data["Плановая дата выполнения"]):
            registration_date = datetime.strptime(user_data["Дата регистрации"], "%Y-%m-%d %H:%M:%S")
            planned_date = registration_date + timedelta(days=30)
            df.loc[df['ID'].astype(str) == user_id, 'Плановая дата выполнения'] = planned_date.strftime("%Y-%m-%d")
            df.to_excel('Рабочая информация.xlsx', sheet_name='Sheet1', index=False)
            user_data["Плановая дата выполнения"] = planned_date.strftime("%Y-%m-%d")

        return user_data
    return None

# Функция start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.message.from_user.username or update.message.from_user.first_name
    user_id = str(update.message.from_user.id)

    add_user(user_id)  # Добавляем пользователя в список при каждом взаимодействии

    # Ваш существующий код для отправки приветствия и взаимодействия
    add_user_to_excel(username, user_id)
    
    # Отправляем GIF и приветствие, как и раньше
    with open('welcome.gif', 'rb') as gif:
        await update.message.reply_animation(animation=gif)
    
    greeting_text = (
        f"Приветствуем {username}! Это бот для работы в команде AllBoost! "
        "Мы занимаемся созданием Ai агентов, продвижением и автоматизацией бизнеса!"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("Стать частью команды AllBoost", callback_data='work'),
            InlineKeyboardButton("Личный кабинет", callback_data='referrals')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(greeting_text, reply_markup=reply_markup)

    # Записываем пользователя в Excel (без номера телефона и даты регистрации)
    add_user_to_excel(username, user_id)

    # Отправляем GIF
    with open('welcome.gif', 'rb') as gif:
        await update.message.reply_animation(animation=gif)

    # Обновленный текст приветствия с именем пользователя
    greeting_text = (
        f"Приветствуем {username}! Это бот для работы в команде AllBoost! "
        "Мы занимаемся созданием Ai агентов, продвижением и автоматизацией бизнеса!"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("Стать частью команды AllBoost", callback_data='work'),
            InlineKeyboardButton("Личный кабинет", callback_data='referrals')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(greeting_text, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)  # Преобразуем ID пользователя в строку

    if query.data == 'referrals':
        work_info = get_work_info(user_id)
        if not work_info.empty:  # Проверяем, пустой ли Series
            response_text = (
                f"Ваш ник: {work_info['Имя пользователя']}\n"
                f"Дата регистрации: {work_info['Дата регистрации']}\n"
                f"Плановая дата выполнения: {work_info['Плановая дата выполнения']}\n"
                f"План на 1 месяц: {work_info['План на 1 месяц']}\n"
                f"Закрыто сделок за 1 месяц: {work_info['Закрыто сделок за 1 месяц']}\n"
                f"Процент выполнения: {work_info['Процент выполнения']}\n"
                f"Выручка от закрытых сделок: {work_info['Выручка от закрытых сделок']}\n"
                f"Общая выручка: {work_info['Общая выручка']}"
            )

            keyboard = [
                [InlineKeyboardButton("Домой", callback_data='home')],
                [InlineKeyboardButton("AllBoost", url="https://t.me/AllBoost_bot")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(text=response_text, reply_markup=reply_markup)
        else:
            await query.edit_message_text(text="Информация о вас не найдена. Пожалуйста, зарегистрируйтесь.")
    
    elif query.data == 'home':
        await query.edit_message_text(text="Вы находитесь на главной странице. Используйте команды для взаимодействия.")
    
    elif query.data == 'work':
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data='register_yes'),
                InlineKeyboardButton("Нет", callback_data='register_no')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Вы готовы зарегистрироваться?", reply_markup=reply_markup)
    
    elif query.data == 'register_yes':
        await query.edit_message_text(text="Сейчас запросим Ваш номер телефона.")
        
        keyboard = [
            [KeyboardButton("Поделиться номером телефона", request_contact=True)]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await query.message.reply_text("Пожалуйста, поделитесь вашим номером телефона:", reply_markup=reply_markup)
        context.user_data['awaiting_phone'] = True
    
    elif query.data == 'register_no':
        await query.edit_message_text(text="Хорошо, если передумаете, просто напишите /start.")

async def handle_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('awaiting_phone') and update.message.contact:
        phone_number = update.message.contact.phone_number
        user_id = update.message.from_user.id
        username = update.message.from_user.username or update.message.from_user.first_name

        # Обновляем номер телефона и дату регистрации в Excel, если пользователь уже существует
        add_user_to_excel(username, user_id, phone_number, registration_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Убираем клавиатуру для запроса номера телефона
        await update.message.reply_text("Спасибо! Ваш номер телефона сохранен.", reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True))

        # Отправляем поздравительное сообщение с кнопкой "Личный кабинет"
        congratulatory_text = (
            "Поздравляем, теперь ты в команде AllBoost. "
            "Заходи в свой личный кабинет и проверь что там есть."
        )
        keyboard = [
            [
                InlineKeyboardButton("Личный кабинет", callback_data='referrals')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(congratulatory_text, reply_markup=reply_markup)
        
        # Сбрасываем состояние ожидания
        context.user_data['awaiting_phone'] = False

# Функция для массовой рассылки
async def send_broadcast(context: ContextTypes.DEFAULT_TYPE, message: str):
    users = load_users()
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

# Команда для массовой рассылки
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        message = ' '.join(context.args)
        await send_broadcast(context, message)
        await update.message.reply_text('Сообщение успешно отправлено всем пользователям.')
    else:
        await update.message.reply_text('Пожалуйста, укажите сообщение для отправки.')

def main() -> None:
    application = ApplicationBuilder().token("7229780590:AAGhyCEXUeuOyViirGdr3qg5URwX0Sr1aTw").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.CONTACT, handle_phone_number))
    
    # Добавляем новый обработчик для команды broadcast
    application.add_handler(CommandHandler("broadcast", broadcast))

    application.run_polling()

if __name__ == '__main__':
    main()
