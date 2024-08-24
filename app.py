from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import pandas as pd
from datetime import datetime

# Создаем экземпляр Flask
app = Flask(__name__)

# Инициализация Telegram Application
app_telegram = Application.builder().token("7229780590:AAGhyCEXUeuOyViirGdr3qg5URwX0Sr1aTw").build()

# Функция для записи пользователя в Excel с добавлением номера телефона и даты регистрации
def add_user_to_excel(username: str, user_id: int, phone_number: str = '', registration_date: str = ''):
    user_id = str(user_id)
    phone_number = str(phone_number)

    try:
        df = pd.read_excel('Пользователи.xlsx', sheet_name='Sheet1')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Имя пользователя", "ID", "номер телефона", "Дата регистрации"])

    if 'номер телефона' in df.columns:
        df['номер телефона'] = df['номер телефона'].astype(str)

    if 'ID' not in df.columns:
        df['ID'] = ''
    if 'номер телефона' not in df.columns:
        df['номер телефона'] = ''
    if 'Дата регистрации' not in df.columns:
        df['Дата регистрации'] = ''

    if user_id not in df['ID'].astype(str).values:
        if not registration_date:
            registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_user = pd.DataFrame([[username, user_id, phone_number, registration_date]], 
                                columns=["Имя пользователя", "ID", "номер телефона", "Дата регистрации"])
        df = pd.concat([df, new_user], ignore_index=True)
    else:
        if phone_number:
            df.loc[df['ID'].astype(str) == user_id, 'номер телефона'] = phone_number
        if registration_date:
            df.loc[df['ID'].astype(str) == user_id, 'Дата регистрации'] = registration_date

    df.to_excel('Пользователи.xlsx', sheet_name='Sheet1', index=False)

# Основная точка входа для вебхуков
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), app_telegram.bot)
    app_telegram.update_queue.put(update)
    return "ok"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.message.from_user.username or update.message.from_user.first_name
    user_id = update.message.from_user.id

    add_user_to_excel(username, user_id)

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

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)

    try:
        df = pd.read_excel('Пользователи.xlsx', sheet_name='Sheet1')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Имя пользователя", "ID", "номер телефона", "Дата регистрации"])

    if query.data == 'referrals':
        if user_id in df['ID'].astype(str).values:
            user_data = df.loc[df['ID'].astype(str) == user_id].iloc[0]
            username = user_data["Имя пользователя"]
            registration_date = user_data["Дата регистрации"]

            try:
                df_links = pd.read_excel('База данных.xlsx')
                link_base = df_links.loc[0, 'Cсылка на базу']
                link_presentation = df_links.loc[0, 'Ссылка на презентацию']
                link_script = df_links.loc[0, 'Cсылка на скрипт']
            except FileNotFoundError:
                link_base = link_presentation = link_script = "Информация недоступна"

            response_text = (
                f"Ваш ник: {username}\n"
                f"Дата регистрации: {registration_date}\n\n"
                f"Cсылка на базу: {link_base}\n"
                f"Ссылка на презентацию: {link_presentation}\n"
                f"Cсылка на скрипт: {link_script}"
            )

            keyboard = [
                [InlineKeyboardButton("Домой", callback_data='home')],
                [InlineKeyboardButton("AllBoost", url="https://t.me/AllBoost_bot")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(text=response_text, reply_markup=reply_markup)
        else:
            keyboard = [
                [
                    InlineKeyboardButton("Да", callback_data='register_yes'),
                    InlineKeyboardButton("Нет", callback_data='register_no')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text="Вы не зарегистрированы. Вы готовы зарегистрироваться?", reply_markup=reply_markup)
    elif query.data == 'home':
        await start(update, context)
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
            [
                KeyboardButton("Поделиться номером телефона", request_contact=True)
            ]
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

        add_user_to_excel(username, user_id, phone_number, registration_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        await update.message.reply_text("Спасибо! Ваш номер телефона сохранен.", reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True))

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
        
        context.user_data['awaiting_phone'] = False

# Регистрация обработчиков
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(CallbackQueryHandler(button))
app_telegram.add_handler(MessageHandler(filters.CONTACT, handle_phone_number))

if __name__ == '__main__':
    app.run(port=8443)
