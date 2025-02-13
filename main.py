import telebot
from telebot import types
import sqlite3

# Подключаемся к базе данных (если файл не существует, он будет создан)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создаем таблицу users, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER UNIQUE,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("База данных и таблица users успешно созданы.")

# Укажите ваш Telegram Bot Token
bot = telebot.TeleBot('')

# Функция для добавления нового пользователя в базу данных
def add_user_to_db(chat_id, first_name, last_name, username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT OR IGNORE INTO users (chat_id, first_name, last_name, username)
        VALUES (?, ?, ?, ?)
        ''', (chat_id, first_name, last_name, username))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        conn.close()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    # Добавляем пользователя в базу данных
    add_user_to_db(chat_id, first_name, last_name, username)

    bot.send_message(chat_id, f"Привет, {first_name}! Ты добавлен в базу данных.")

# Запуск бота
bot.infinity_polling()
