from flask import Flask, request, render_template_string
from db import connect

app = Flask(__name__)

@app.route('/')
def index():
    user_id = request.args.get('user_id')
    
    if user_id:
        conn = connect()
        if conn:
            cursor = conn.cursor()
            
            # Проверка, существует ли пользователь в базе данных
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()

            if not result:
                # Если пользователь не найден, добавляем его
                cursor.execute("INSERT INTO users (user_id) VALUES (%s)", (user_id,))
                conn.commit()

            cursor.close()
            conn.close()

        # Отображаем приветственную страницу
        return render_template_string('<img src="welcome.gif" alt="Welcome to AllBoost-job">')
    else:
        return "User ID not provided."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
