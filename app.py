from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешаем CORS

# Функция для получения всех chat_id из базы данных
def get_all_chat_ids():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id FROM users")
        chat_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        print(f"[LOG] Найдено chat_ids: {chat_ids}")
        return chat_ids
    except Exception as e:
        print(f"[ERROR] Ошибка при получении chat_ids: {e}")
        return []

# API для получения всех chat_id
@app.route('/api/get_chat_ids', methods=['GET'])
def get_chat_ids():
    try:
        chat_ids = get_all_chat_ids()
        if not chat_ids:
            print("[LOG] chat_ids пустой")
        return jsonify({'chat_ids': chat_ids}), 200
    except Exception as e:
        print(f"[ERROR] Ошибка при обработке запроса /api/get_chat_ids: {e}")
        return jsonify({'error': 'Ошибка при получении chat_ids'}), 500

if __name__ == '__main__':
    print("[LOG] Запуск сервера Flask на http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
