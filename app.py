from flask import Flask, request, render_template_string
from db import add_or_update_user

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    
    user_id = update['message']['from']['id']
    username = update['message']['from'].get('username', 'Unknown')
    phone = update['message']['contact']['phone_number'] if 'contact' in update['message'] else None
    
    # Добавляем или обновляем пользователя в базе данных
    add_or_update_user(user_id, username, phone)
    
    return "OK", 200

@app.route('/')
def index():
    return render_template_string('<img src="welcome.gif" alt="Welcome to AllBoost-job">')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
