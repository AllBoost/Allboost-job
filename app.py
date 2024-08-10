from flask import Flask, request, render_template_string
from db import connect
import requests

app = Flask(__name__)
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

@app.route('/start')
def start():
    user_id = request.args.get('user_id')
    if user_id:
        user_info = requests.get(f'https://api.telegram.org/bot{TOKEN}/getChat?chat_id={user_id}').json()
        username = user_info['result']['username']
        phone_number = user_info.get('phone_number', 'Not provided')

        conn = connect()
        if conn:
            cursor = conn.cursor()
            
            # Проверка, существует ли пользователь в базе данных
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()

            if not result:
                # Если пользователь не найден, добавляем его
                cursor.execute("INSERT INTO users (user_id, username, phone_number) VALUES (%s, %s, %s)",
                               (user_id, username, phone_number))
                conn.commit()

            cursor.close()
            conn.close()

        return render_template_string('<img src="welcome.gif" alt="Welcome to AllBoost-job">')
    else:
        return "User ID not provided."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
