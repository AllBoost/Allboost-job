import mysql.connector
from config import db_host, db_name, db_user, db_pass

def connect():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def add_or_update_user(user_id, username, phone=None):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        
        # Проверка, существует ли пользователь в базе данных
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()

        if not result:
            # Если пользователь не найден, добавляем его
            cursor.execute("INSERT INTO users (user_id, username, phone) VALUES (%s, %s, %s)", (user_id, username, phone))
        else:
            # Если пользователь найден, обновляем его данные
            cursor.execute("UPDATE users SET username = %s, phone = %s WHERE user_id = %s", (username, phone, user_id))

        conn.commit()
        cursor.close()
        conn.close()
